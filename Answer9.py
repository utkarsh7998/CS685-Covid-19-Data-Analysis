#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)


# In[2]:


df=pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory=False)
# df.head()


# In[3]:


# df.shape


# # Deleting columns which don't have male and female vaccinated

# In[4]:


x = list(df.iloc[0])

# for i in range(len(x)):
#     print(i,":",x[i])



# In[5]:


#finding columns to be dropped
indexes_to_be_deleted =[]
for i in range(6,2896):
    if i%10==9:
        continue
    indexes_to_be_deleted.append(i)

#dropping the columns stored in columns_to_be_deleted list
df.drop(df.columns[indexes_to_be_deleted], axis = 1, inplace = True)
# df


# In[6]:


# for i in range(len(df.columns)):
#     print(i,":",df.columns[i])


# In[7]:


#finding columns to be dropped
indexes_to_be_deleted =list(range(6,209))
indexes_to_be_deleted.append(list(range(217,295)))

#dropping the columns stored in columns_to_be_deleted list
df.drop(df.columns[list(range(217,295))], axis = 1, inplace = True)

# df


# In[8]:


df.drop(df.columns[list(range(6,209))], axis = 1, inplace = True)
# df


# # Fill  missing NaN values with 0

# In[9]:


#filling missing NAN values with 0
df.fillna(0,inplace=True)
# df.isna().sum()


# # Drop first row because it contains headings

# In[10]:


#dropping first row
df = df.iloc[1:,:]
# df.head()


# # Adding no of doses in last week as column

# In[11]:


# df 
df['Last Week Doses'] = df['14/08/2021.3'].astype('int64') - df['07/08/2021.3'].astype('int64')
# df


# In[12]:

df1 = df.copy()
df1 = df1[['State_Code','Last Week Doses','14/08/2021.3']]
df1.reset_index(drop=True,inplace=True)
df1['14/08/2021.3'] = df1['14/08/2021.3'].astype('int64')
# df1


# # Grouping the states  and summing their values

# In[13]:


dft = df1.groupby('State_Code')[['14/08/2021.3','Last Week Doses',]].agg('sum')
dft['State'] = dft.index
dft.reset_index(drop=True,inplace=True)
dft.rename({'State_Code':'State_Key','14/08/2021.3':'Total Doses'},axis=1,inplace=True)
dft = dft[['State','Last Week Doses','Total Doses']]

# dft


# # Reading Population Data

# In[14]:


population = pd.read_excel("DDW_PCA0000_2011_Indiastatedist.xlsx",engine='openpyxl')
# population.head()


# # Preprocessing Census data: removing columns and adding ratio, state codes

# In[15]:


def sc(i):
    name = ['IN','JK','HP','PB','CH','UT','HR','DL','RJ','UP','BR',
            'SK','AR','NL','MN','MZ','TR','ML','AS','WB','JH',
            'OR','CT','MP','GJ','DN','DN','MH','AP','KA','GA',
            'LD','KL','TN','PY','AN']
    return name[i]

state = population.copy()
state = state[(state['Level']=='STATE')&(state['TRU']=='Total')]

state.rename({'State':'State_Key'},axis=1,inplace=True)
state['State_Key'] = state['State_Key'].apply(lambda x: sc(x))
state = state[['State_Key','TOT_P']]
state.reset_index(drop=True,inplace=True)


# state


# # grouping the states in census data because daman and diu and dadra and nagar haveli have been merged

# In[16]:


state = state.groupby(['State_Key'])[['TOT_P']].agg('sum')
state['State_Key'] = state.index
state.reset_index(drop=True,inplace=True)
# dft.rename({'State_Code':'State_Key'},axis=1,inplace=True)
# state


# In[17]:


# population[(population['Level']=='STATE')&(population['TRU']=='Total')]


# # Merge census and vaccination data to get population

# In[18]:


dft.rename({'State':'State_Key'},axis=1,inplace=True)
x = pd.merge(dft,state,on=['State_Key'])
# x


# In[19]:


import datetime
x['Last Week Rate'] = x['Last Week Doses']/7
x['Population Left'] = abs(x['TOT_P'] - x['Total Doses'])
# x['Population Left'] = x['TOT_P'] - x['Total Doses']
import math
# x['Population Left'] = x['Population Left'].astype(float)
x['No of days'] = x['Population Left']/x['Last Week Rate']
# x[] = x['TOT_P'] - x['Total Doses']
x['No of days'] = x['No of days'].apply(lambda x: math.ceil(x))
x['date'] = datetime.date(2021, 8, 14)
# x


# In[20]:


x['Destiny'] =  0
x['No of days'] = x['No of days'].astype('int')
x.reset_index(drop=True,inplace=True)
for i in range (len(x)):
    d = x.loc[i,'No of days']
    x.loc[i,'Destiny'] = (x.loc[i,'date'] + pd.DateOffset(days=int(d))).strftime(format='%d/%m/%Y')
# x


# In[21]:


ans1 = x.copy()
ans1 = ans1[['State_Key','Population Left','Last Week Rate','Destiny']]
ans1.rename({'State_Key':'stateid','Population Left':'populationleft','Last Week Rate': 'rateofvaccination','Destiny':'date'},axis=1,inplace=True)
# ans1.sort_values('vaccinateddose1ratio',inplace=True)
ans1.reset_index(drop=True,inplace=True)
# ans1


# In[22]:


ans1.to_csv('complete-vaccination.csv',index=False)


# In[23]:


print("Execution Completed Successfully")


# In[ ]:




