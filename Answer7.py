#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)


# In[14]:


df=pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory=False)
# df


# In[15]:


index_to_del =[]
for i in range(6,2896):
    if (i%10!=4 and i%10!=5):
        index_to_del.append(i)
df.drop(df.columns[index_to_del], axis = 1, inplace = True)
df.drop(['S No','State','Cowin Key','District'],axis=1, inplace=True)
df =df.iloc[1:,:]
# df


# In[16]:


x=df.columns
# for i in range(len(x)):
#     print(i,":",x[i])
df=df.iloc[:,0:424]
# df


# In[17]:


df.fillna(0,inplace=True)
# df


# In[18]:


col=df.columns
i=1
for (index, row) in df.iterrows():
#     print(i)
    for j in range(4,len(row.values),1):
        prev =  int(row.values[j-2])
        curr =  int(row.values[j])
        curr=max(prev,curr)

        df.at[index,col[j]] = curr
    i=i+1


# In[19]:


df=df[['State_Code','District_Key','14/08/2021.8','14/08/2021.9']]
# df


# In[20]:


df['14/08/2021.9']= df['14/08/2021.9'].astype(int)
df['14/08/2021.8'] = df['14/08/2021.8'].astype(int)
try:
    df['Ratio'] =df['14/08/2021.9']/df['14/08/2021.8']
except:
    pass
# df


# # Writing output districtwise

# In[21]:


df2=df.copy()
df2 = df2[['District_Key','Ratio']]
df2.sort_values('Ratio',inplace=True)
df2.to_csv('district-vaccine-type-ratio.csv',index=False)


# # Writing output statewise

# In[22]:


df3=df.copy()
df3=df3[['State_Code','14/08/2021.8','14/08/2021.9']]
df3 = df3.groupby('State_Code').agg('sum')
df3['14/08/2021.9']= df3['14/08/2021.9'].astype(int)
df3['14/08/2021.8'] = df3['14/08/2021.8'].astype(int)
try:
    df3['Ratio'] =df3['14/08/2021.9']/df3['14/08/2021.8']
except:
    pass

df3.rename({'14/08/2021.8': 'Covaxin', '14/08/2021.9': 'Covishield'}, axis=1, inplace=True)

df3.sort_values('Ratio',inplace=True)

df3.to_csv('state-vaccine-type-ratio.csv')


# # Writing overall output

# In[23]:


df4=df.copy()
df4=df4[['State_Code','14/08/2021.8','14/08/2021.9']]
df4['State_Code'] = 'India'
df4 = df4.groupby('State_Code').agg('sum')
df4['14/08/2021.9']= df4['14/08/2021.9'].astype(int)
df4['14/08/2021.8'] = df4['14/08/2021.8'].astype(int)
# try:
df4['vaccineratio'] =df4['14/08/2021.9']/df4['14/08/2021.8']
# except:
#     pass

df4.rename({'14/08/2021.8': 'Covaxin', '14/08/2021.9': 'Covishield'}, axis=1, inplace=True)

df4.sort_values('vaccineratio',inplace=True)
df4['Overallid'] = 'India'
df4.reset_index(drop=True,inplace=True)
df4 = df4[['Overallid','vaccineratio']]

df4.to_csv('overall-vaccine-type-ratio.csv',index=False)
# df4


# In[24]:


print("Execution completed successfully")


# In[ ]:




