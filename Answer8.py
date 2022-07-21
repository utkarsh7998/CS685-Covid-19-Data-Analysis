#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)


# In[53]:


df=pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory=False)
# df.head()


# In[54]:


# df.shape


# # Deleting columns which don't have male and female vaccinated

# In[55]:


x = list(df.iloc[0])
# for i in range(len(x)):
#     print(i,":",x[i])

#finding columns to be dropped
indexes_to_be_deleted =[]
for i in range(6,2896):
    if i%10==9 or i%10==0:
        continue
    indexes_to_be_deleted.append(i)

#dropping the columns stored in columns_to_be_deleted list
df.drop(df.columns[indexes_to_be_deleted], axis = 1, inplace = True)
# df


# # Fill  missing NaN values with 0

# In[56]:


#filling missing NAN values with 0
df.fillna(0,inplace=True)
# df.isna().sum()


# # District names to lowercase

# In[57]:


#making district names as lowercase
df['District'] = df['District'].str.lower()
# df
# type(df['District'])


# ## Dropping columns beyong column 428 -i.e- 14 AUG 2021

# In[58]:


x = df.columns
indexes_to_be_deleted = []
# for i in range(len(x)):
#     print(i,x[i])
indexes_to_be_deleted = range(428,584,1)
#dropping the columns stored in columns_to_be_deleted list
df.drop(df.columns[indexes_to_be_deleted], axis = 1, inplace = True)
# df


# # Drop first row because it contains headings

# In[59]:


#dropping first row
df = df.iloc[1:,:]
# df.head()


# # Drop Sno column

# In[60]:


df = df.drop(['S No'],axis=1)
# df.head()


# # making rows : for each date for each district in a dataframe

# In[61]:


df.reset_index(drop=True,inplace=True)
df1 = pd.DataFrame()
for i in range(len(df)):
#     print(df.iloc[i]['District_Key'],df.loc[i]['14/08/2021.5'])
    t = {} #empty dictionary
    t['District_Key'] = df.iloc[i]['District_Key']
    t['Dose1'] = df.loc[i]['14/08/2021.3'] #males vaccinated till 14-aug-2021 
    t['Dose2'] = df.loc[i]['14/08/2021.4'] #females vaccinated till 14-aug-2021
    t['State'] = df.loc[i]['State']
#     print(t)
    df1 = df1.append(t,ignore_index=True)
    


# # Find district keys having duplicates and sum them up.

# In[62]:


# finding duplicate rows
# print(df1['District_Key'].value_counts())
# print(df1['District_Key'].value_counts().value_counts())


# # Changing values to integer

# In[63]:


df1['Dose1'] = df1['Dose1'].astype('int64')
df1['Dose2'] = df1['Dose2'].astype('int64')


# In[64]:


dft = df1.groupby(['District_Key','State'])[['Dose1','Dose2']].agg('sum')
dft['State'] = dft.index.to_numpy()
dft['District_Key'] = dft.index.to_numpy()
dft['State'] = dft['State'].apply(lambda x: x[1])
dft['District_Key'] = dft['District_Key'].apply(lambda x: x[0])
dft.reset_index(drop=True,inplace=True)
dft = dft[['District_Key','State','Dose1','Dose2']]

# dft


# In[65]:


# Verifying if duplicate rows are finally removed or not
# print(dft['District_Key'].value_counts())
# print(dft['District_Key'].value_counts().value_counts())


# # Reading Population Data

# In[ ]:


population = pd.read_excel("DDW_PCA0000_2011_Indiastatedist.xlsx",engine='openpyxl')
# population.head()


# # Preprocessing Census data: removing columns and adding ratio, state codes

# In[ ]:


def sc(i):
    name = ['IN','JK','HP','PB','CH','UT','HR','DL','RJ','UP','BR',
            'SK','AR','NL','MN','MZ','TR','ML','AS','WB','JH',
            'OR','CT','MP','GJ','DD','DD','MH','AP','KA','GA',
            'LD','KL','TN','PY','AN']
    return name[i]
population = population.drop(['District','Subdistt','Town/Village','Ward','EB'],axis=1)
population.drop(population.iloc[:, 8:89], inplace = True, axis = 1)
population.drop(population.iloc[:, 4:5], inplace = True, axis = 1)
population = population[population['TRU']=='Total']
population = population.drop(['TRU'],axis=1)
population['Population Ratio'] = population['TOT_F']/population['TOT_M']
population.reset_index(drop=True,inplace=True)
population['State'] = population['State'].apply(lambda x: sc(x))
population.rename({'State':'State_Key'},axis=1,inplace=True)
# population.head()


# In[ ]:


# population[population['Level']=='STATE']


# # Constructing Statewise, Districtwise and India wise dataframes
# 

# In[ ]:


state = population[population['Level']=='STATE'].reset_index()
country = population[population['Level']=='India'].reset_index()
district = population[population['Level']=='DISTRICT'].reset_index()
# district
# state.shape[0]+country.shape[0]+district.shape[0]


# # Districtwise Analysis

# In[ ]:



district.rename({'Name':'District'},axis=1,inplace=True)
district.reset_index(drop=True, inplace=True)
# district


# In[ ]:


district['District'] = district['District'].apply(lambda x: x.lower().strip())
# district['District'] = district['District'].apply(lambda x: x.split(' ')[0])
# district


# In[ ]:


# state


# In[ ]:


# district[district['District']=='east district']


# # Merging census and vaccine dataframes

# In[ ]:


df1 = dft.copy()
#Adding District Name and State Code as columns
df1['District'] = df1['District_Key'].apply(lambda x: x.split('_')[1])
df1['State_Key'] = df1['District_Key'].apply(lambda x: x.split('_')[0])
# df1


# In[ ]:


# making District name as lowercase and strip
dfx=df1.copy()
dfx['District'] = dfx['District'].apply(lambda x: x.lower().strip())
# district['District'] = district['District'].apply(lambda x: x.split(' ')[0])
# dfx


# ## Finding common and uncommon districts

# In[ ]:


s1 = set(district['District'].unique())
s2 = set(dfx['District'].unique())
# print("common districts: ",len(s2.intersection(s1)))
# print("only s1 districts: ",len(s1.difference(s2)))
# print("only s2 districts: ",len(s2.difference(s1)))


# In[ ]:


onlys1 = set(s1.difference(s2))
onlys2 = set(s2.difference(s1))


# ## Creating function to rectify spelling mistakes in names

# In[ ]:


# district


# In[ ]:


# Finding state names to check for multiple names in different states
m = pd.DataFrame()
for i in onlys1:
    m=m.append(district[district['District']==i][['State_Key','District']])
# m.shape


# In[ ]:


# m.head(50)


# In[ ]:


# m.tail(49)


# In[ ]:


# onlys2


# In[ ]:


def corrected_name(x):
    if x== 'ahmadabad':x='ahmedabad'
    if x== 'ahmadnagar' :x='ahmednagar'
    if x== 'allahabad' : x='prayagraj'
    if x== 'anugul' : x='angul'
    if x== 'badgam' : x='budgam'
    if x== 'bagalkot' : x='bagalkote'
#     if x== 'baleshwar' : x= #not found
    if x== 'banas kantha' : x='banaskantha'
    if x== 'bandipore' : x='bandipora'
    if x== 'bangalore' : x=  'bengaluru urban'
    if x== 'bangalore rural' : x='bengaluru rural'
    if x== 'bara banki' : x='barabanki'
    if x== 'baramula' : x='baramulla'
    if x== 'barddhaman' : x='purba bardhaman'
    if x== 'baudh' : x='boudh'
    if x== 'belgaum' : x='belagavi'
    if x== 'bellary' : x='ballari'
    if x== 'bid' : x='beed'
    if x== 'buldana' : x='buldhana'
    if x== 'central' : x='central delhi'
    if x== 'chamarajanagar' : x= 'chamarajanagara'
    if x== 'chikmagalur' : x= 'chikkamagaluru'
    if x== 'chittaurgarh' : x= 'chittorgarh'
    if x== 'dadra & nagar haveli' : x= 'dadra and nagar haveli'
    if x== 'darjiling' : x= 'darjeeling'
    if x== 'debagarh' : x= 'deogarh'
    if x== 'dhaulpur' : x= 'dholpur'
#     if x== 'dibang valley' : x=
    if x== 'dohad' : x= 'dahod'
    if x== 'east' : x='east delhi'
    if x== 'east district' : x= 'east sikkim'
    if x== 'faizabad' : x= 'ayodhya'
    if x== 'firozpur' : x= 'ferozepur'
    if x== 'garhwal' : x= 'pauri garhwal'
    if x== 'gondiya' : x= 'gondia'
    if x== 'gulbarga' : x= 'kalaburagi'
    if x== 'gurgaon' : x= 'gurugram'
    if x== 'haora' : x= 'howrah'
    if x== 'hardwar' : x= 'haridwar'
    if x== 'hugli' : x= 'hooghly'
    if x== 'jagatsinghapur' : x= 'jagatsinghpur'
    if x== 'jaintia hills' : x='west jaintia hills'
    if x== 'jajapur' : x='jajpur'
    if x== 'jalor' : x='jalore'
    if x== 'janjgir - champa' : x= 'janjgir champa'
    if x== 'jhunjhunun' : x= 'jhunjhunu'
    if x== 'jyotiba phule nagar' : x='amroha'
    if x== 'kachchh' : x='kutch'
    if x== 'kaimur (bhabua)' : x='kaimur'
    if x== 'kanniyakumari' : x= 'kanyakumari'
    if x== 'kanshiram nagar' : x= 'kasganj'
    if x== 'khandwa (east nimar)' : x='khandwa'
    if x== 'khargone (west nimar)' : x='khargone'
    if x== 'kheri' : x= 'lakhimpur kheri'
    if x== 'koch bihar' : x= 'cooch behar'
    if x== 'kodarma' : x= 'koderma'
    if x== 'lahul & spiti' : x= 'lahaul and spiti'
    if x== 'leh(ladakh)' : x= 'leh'
    if x== 'mahamaya nagar' : x= 'hathras'
    if x== 'mahbubnagar' : x= 'mahabubnagar'
    if x== 'mahesana' : x= 'mehsana'
    if x== 'mahrajganj' : x= 'maharajganj'
    if x== 'maldah' : x= 'malda'
    if x== 'mewat' : x='nuh'
    if x== 'muktsar' : x= 'sri muktsar sahib'
#     if x== 'mumbai suburban' : x=
    if x== 'mysore' : x= 'mysuru'
    if x== 'narsimhapur' : x= 'narsinghpur'
    if x== 'north' : x= 'north delhi'
    if x== 'north  & middle andaman' : x= 'north and middle andaman'
    if x== 'north  district' : x= 'north sikkim'
    if x== 'north east' : x= 'north east delhi'
    if x== 'north twenty four parganas' : x= 'north 24 parganas'
    if x== 'north west' : x= 'north west delhi'
    if x== 'panch mahals' : x= 'panchmahal'
    if x== 'pashchim champaran' : x= 'west champaran'
    if x== 'pashchimi singhbhum' : x= 'west singhbhum'
    if x== 'purba champaran' : x= 'east champaran'
    if x== 'purbi singhbhum' : x= 'east singhbhum'
    if x== 'puruliya' : x= 'purulia'
    if x== 'rangareddy' : x= 'ranga reddy'
    if x== 'sabar kantha' : x= 'sabarkantha'
    if x== 'sahibzada ajit singh nagar' : x= 's.a.s. nagar'
    if x== 'sant ravidas nagar (bhadohi)' : x= 'bhadohi'
    if x== 'shimoga' : x= 'shivamogga'
    if x== 'shupiyan' : x= 'shopiyan'
    if x== 'south' : x= 'south delhi'
    if x== 'south district' : x='south sikkim'
    if x== 'south twenty four parganas' : x= 'south 24 parganas'
    if x== 'south west' : x= 'south west delhi'
    if x== 'sri potti sriramulu nellore' : x= 's.p.s. nellore'
    if x== 'the dangs' : x= 'dang'
    if x== 'the nilgiris' : x= 'nilgiris'
    if x== 'tumkur' : x= 'tumakuru'
    if x== 'warangal' : x= 'warangal rural'
    if x== 'west' : x= 'west delhi'
    if x== 'west district' : x='west sikkim'
    if x== 'y.s.r.' : x= 'y.s.r. kadapa'
    return x


# # Applying corrected name function on district dataframe

# In[ ]:


district['District'] = district['District'].apply(lambda x: corrected_name(x))
# district


# # Find common and uncommon names after coorecting names

# In[ ]:


s1 = set(district['District'].unique())
s2 = set(dfx['District'].unique())
# print("common districts: ",len(s2.intersection(s1)))
# print("only s1 districts: ",len(s1.difference(s2)))
# print("only s2 districts: ",len(s2.difference(s1)))


# # Find duplicate district names in census data

# In[ ]:


# k = pd.DataFrame(district[['State_Key','District']].value_counts())
# print('Based on State_Key and District:\n', district[['State_Key','District']].value_counts().value_counts())
# print('Based on only District:\n', district[['District']].value_counts().value_counts())
# print("that means we will merge on basis of state_key and district because it has unique values")


# # Merging population and vaccine data

# In[ ]:


x = pd.merge(dfx,district,on=['District','State_Key'])
x['Dose1 Ratio'] = x['Dose1'].astype('int64') /x['TOT_P'].astype('int64')
x['Dose2 Ratio'] = x['Dose2'].astype('int64') /x['TOT_P'].astype('int64')
# x['Ratioofratios'] = x['Vaccination Ratio']/x['Population Ratio']
# x


# In[ ]:


ans1 = x.copy()
ans1 = ans1[['District_Key','Dose1 Ratio','Dose2 Ratio']]
ans1.rename({'District_Key':'districtid','Dose1 Ratio':'vaccinateddose1ratio','Dose2 Ratio':'vaccinateddose2ratio'},axis=1,inplace=True)
ans1.sort_values('vaccinateddose1ratio',inplace=True)
ans1.reset_index(drop=True,inplace=True)
# ans1


# In[ ]:


ans1.to_csv('district-vaccinated-dose-ratio.csv',index=False)


# # Districtwise Analysis Completed

# # Statewise Analysis

# In[ ]:


# state


# In[ ]:


# dfx


# In[ ]:


df3 = dfx.copy()
df3 = df3[['State_Key','Dose1','Dose2']]
df3 = df3.groupby(['State_Key'])[['Dose1','Dose2']].agg('sum')
df3['State_Key'] = df3.index.to_numpy()
df3.reset_index(drop=True, inplace=True)
df3 = df3[['State_Key','Dose1','Dose2']]
# df3


# In[ ]:


ans2 = pd.merge(df3,state,on=['State_Key'])
ans2['Dose1 Ratio'] = ans2['Dose1']/ans2['TOT_P']
ans2['Dose2 Ratio'] = ans2['Dose2']/ans2['TOT_P']
ans2 = ans2[['State_Key','Dose1 Ratio','Dose2 Ratio']]
ans2.rename({'State_Key':'stateid','Dose1 Ratio':'vaccinateddose1ratio','Dose2 Ratio':'vaccinateddose2ratio'},axis=1,inplace=True)
ans2.sort_values('vaccinateddose1ratio',inplace=True)
ans2.reset_index(drop=True, inplace=True)


# In[ ]:



ans2.to_csv('state-vaccinated-dose-ratio.csv',index=False)


# # Statewise Analysis Completed
# 

# # Overall Analysis

# In[ ]:


# country


# In[ ]:


# df3


# In[ ]:


# df3['Dose1'].sum()
# df3['Dose2'].sum()
# country.loc[0]['TOT_P']


# In[ ]:


df4 = pd.DataFrame()
t = {}
t['overallid'] = 'India'
t['vaccinateddose1ratio'] = df3['Dose1'].sum()/country.loc[0]['TOT_P']

t['vaccinateddose2ratio'] = df3['Dose2'].sum()/country.loc[0]['TOT_P']
df4 = df4.append(t,ignore_index=True)
df4 = df4[['overallid','vaccinateddose1ratio','vaccinateddose2ratio']]
ans3 = df4.copy()
# ans3


# In[ ]:


ans3.to_csv('overall-vaccinated-dose-ratio.csv',index=False)


# # Overall Analysis Completed

# In[ ]:


print("Execution completed successfully")


# In[ ]:




