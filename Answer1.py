#!/usr/bin/env python
# coding: utf-8

# In[21]:


import numpy as np
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)


# In[22]:


f = open('neighbor-districts.json',)
d = json.load(f)
# d


# In[23]:


def corrected_name( x ):
    if(x=="aizwal"):
        x = "aizawl"
    if(x=='anugul'):
        x = 'angul'
    if(x=='ashok nagar'):
        x = 'ashoknagar'
    if(x=='badgam'):
        x = 'budgam'
    if(x=='baleshwar'):
        x = 'bageshwar'
    if(x=='banas kantha'):
        x = 'banaskantha'
    if(x=='bangalore rural'):
        x = 'bengaluru rural'
    if(x=='bangalore urban'):
        x = 'bengaluru urban'
    if(x=='baramula'):
        x = 'baramulla'
    if(x=='baudh'): 
        x = 'boudh'
    if(x=='belgaum'): 
        x = 'belagavi'
    if(x=='bellary'):
        x = 'ballari'
    if(x=='bemetara'):
        x = 'bametara'
    
    if(x=='bid'):
        x = 'beed'
    
    if(x=='bishwanath'):
        x = 'biswanath'

    if(x=='chamarajanagar'):
        x = 'chamarajanagara'
    if(x=='dantewada'):
        x = 'dakshin bastar dantewada'
    if(x=='debagarh'):
        x = 'deogarh'
    
    if(x=='devbhumi dwaraka'): 
        x = 'devbhumi dwarka'
    if(x=='dhaulpur'):
        x = 'dholpur'

    if(x=='east karbi anglong'):
        x = 'karbi anglong'
    if(x=='faizabad'):
        x = 'ayodhya'
    if(x=='fategarh sahib'):
        x = 'fatehgarh sahib'
    if(x=='firozpur'):
        x = 'ferozepur'
    if(x=='gondiya'):
        x = 'gondia'
    
    if(x=='hugli'):
        x = 'hooghly'
    if(x=='jagatsinghapur'):
        x = 'jagatsinghpur'
    if(x=='jajapur'):
        x = 'jajpur'
    if(x=='jalor'):
        x = 'jalore'
    if(x=='janjgir-champa'):
        x = 'janjgir champa'
    if(x=='jhunjhunun'):
        x = 'jhunjhunu'
    if(x=='jyotiba phule nagar'):
        x = 'amroha'
    if(x=='kabirdham'):
        x = 'kabeerdham'
    if(x=='kaimur (bhabua)'):
        x = 'kaimur'
    if(x=='kanchipuram'):
        x = 'kancheepuram'
#     if(x=='kheri'):
#         x = 'lakhimpur kheri'
    if(x=='kochbihar'):
        x = 'cooch behar'
    if(x=='kodarma'):
        x = 'koderma'
    if(x=='komram bheem'):
        x = 'komaram bheem'
#     if(x=='konkan division'): #not found
#         x = 'konkan division'
    if(x=='lahul and spiti'):
        x = 'lahaul and spiti'
    if(x=='mahesana'): 
        x = 'mehsana'
    if(x=='mahrajganj'):
        x = 'maharajganj'
    if(x=='maldah'):
        x = 'malda'
    if(x=='marigaon'):
        x = 'morigaon'
    if(x=='medchal–malkajgiri'):
        x = 'medchal malkajgiri'
    if(x=='muktsar'):
        x = 'sri muktsar sahib'
    if(x=='mumbai city'):
        x = 'mumbai'
    if x== 'mumbai suburban':
        x = 'mumbai'
    if x== 'nandubar':
        x = 'nandurbar'
    if x== 'narsimhapur':
        x = 'narsinghpur'
    if x== 'nav sari':
        x = 'navsari'

    if x== 'noklak': #not found
        x = 'noklak'
    if x=='new delhi' : #dealing with all delhi here
        x = 'new delhi'
    if(x=='east delhi'):
        x = "new delhi"
    if x== 'north delhi':
        x = 'new delhi'
    if(x=='central delhi'):
        x = 'new delhi'
    if x== 'north east delhi':
        x = 'new delhi'
    if x== 'north west delhi':
        x = 'new delhi'
    if x== 'south delhi':
        x = 'new delhi'
    if x== 'south east delhi':
        x = 'new delhi'
    if x== 'south west delhi':
        x = 'new delhi'      #delhi completed
    if x== 'pakaur':
        x = 'pakur'
    if x== 'palghat':
        x = 'palghar'
    if x== 'panch mahal':
        x = 'panchmahal'
    if x== 'pashchim champaran':
        x = 'west champaran'
    if x== 'pashchimi singhbhum':
        x = 'west singhbhum'
#     if x== 'pattanamtitta':
#         x = 'pathanamthitta'
    if x== 'purba champaran':
        x = 'east champaran'
    if x== 'purbi singhbhum':
        x = 'east singhbhum'
    if x== 'puruliya':
        x = 'purulia'
    if x== 'rae bareilly':
        x = 'rae bareli'
    if x== 'rajauri':
        x = 'rajouri'
    if x== 'rangareddy':
        x = 'ranga reddy'
    if x== 'ri-bhoi':
        x = 'ribhoi'
    if x== 'sabar kantha':
        x = 'sabarkantha'
    if x== 'sahibzada ajit singh nagar':
        x = 's.a.s. nagar'
    if x== 'sait kibir nagar':
        x = 'sant kabir nagar'
    if x== 'sant ravidas nagar':
        x = 'bhadohi'
    if x== 'sepahijala':
        x = 'sipahijala'
    if x== 'seraikela kharsawan':
        x = 'saraikela-kharsawan'
    if x== 'shahdara': 
        x = 'new delhi'
    if x== 'shaheed bhagat singh nagar':
        x = 'shahid bhagat singh nagar'
    if x== 'sharawasti':
        x = 'shrawasti'
    if x== 'shimoga':
        x = 'shivamogga'
    if x== 'shopian':
        x = 'shopiyan'
    if x== 'siddharth nagar':
        x = 'siddharthnagar'
    if x== 'sivagangai':
        x = 'sivaganga'
    if x== 'sonapur':
        x = 'subarnapur'

    if x== 'south salmara-mankachar':
        x = 'south salmara mankachar'

    if x== 'sri ganganagar':
        x = 'ganganagar'
    if x== 'sri potti sriramulu nellore':
        x = 's.p.s. nellore'
    if x== 'the dangs':
        x = 'dang'
    if x== 'the nilgiris':
        x = 'nilgiris'
    if x== 'thoothukudi':
        x = 'thoothukkudi'
    if x== 'tiruchchirappalli':
        x = 'tiruchirappalli'
    if x== 'tirunelveli kattabo':
        x = 'tirunelveli'
    if x== 'tiruvanamalai':
        x = 'tiruvannamalai'
    if x== 'tumkur':
        x = 'tumakuru'
    if x== 'west delhi':
        x = 'new delhi'
    if x== 'yadagiri':
        x = 'yadadri bhuvanagiri'
    if x== 'ysr':
        x = 'y.s.r. kadapa'
    return x


# # Converting the json to a dataframe

# In[24]:


arr = []
districts_sir = set()
for key,value in d.items():
    x = ""
    x = key.split('/')[0]
    x = x.replace("_district","")
    x = x.replace("_"," ")
    x = corrected_name(x)
    if x=='konkan division' or x=='niwari' or x=='noklak' or x=='kheri' or x=='Parbhani' or x=='pattanamtitta':
        continue
    districts_sir.add(x)
    temp = []
    for i in value:
        i = i.split('/')[0]
        i = i.replace("_district","")
        i = i.replace("_"," ")
        i = corrected_name(i)
        if i=='konkan division' or i=='niwari' or i=='noklak' or i=='kheri' or i=='parbhani' or i=='pattanamtitta' or i==x:
                continue
        temp.append(i)
        districts_sir.add(i)
    arr.append({'District':x ,'Neighbors':temp })


# In[25]:


df = pd.DataFrame(arr)
df['Neighbors'] = df['Neighbors'].apply(lambda x: str(x).replace('[', '').replace(']', '').replace("'", ""))
# df


# In[26]:


# districts_sir # set of districts given by sir


# # Finding all common districts from vaccination and covid data

# ## 1. Vaccination Data : cowin_vaccine_data_districtwise.csv

# In[27]:


vaccine = pd.read_csv('cowin_vaccine_data_districtwise.csv',header=0,low_memory=False)
vaccine = vaccine.iloc[1:,:]
vaccine = vaccine[['District_Key','District','State_Code']]
vaccine['District'] = vaccine['District'].str.lower()
# vaccine


# In[28]:


x2 = set(vaccine['State_Code'].unique())
# x2


# In[29]:


# # Checking duplicates
# print("Before removing duplicates:")
# print(vaccine[['District','District_Key']].value_counts().value_counts())

vaccine.drop_duplicates(subset =["District_Key","District"],keep = 'first', inplace = True)
# print("After removing duplicates:")
# print(vaccine[['District','District_Key']].value_counts().value_counts())


# ## 2. Covid data: districts.csv

# In[30]:


statekey ={'Andaman and Nicobar Islands':'AN',
 'Andhra Pradesh':'AP',
 'Arunachal Pradesh':'AR',
 'Assam':'AS',
 'Bihar':'BR',
 'Chandigarh':'CH',
 'Chhattisgarh':'CT',
 'Dadra and Nagar Haveli and Daman and Diu':'DN',
 'Delhi':'DL',
 'Goa':'GA',
 'Gujarat':'GJ',
 'Haryana':'HR',
 'Himachal Pradesh':'HP',
 'Jammu and Kashmir':'JK',
 'Jharkhand':'JH',
 'Karnataka':'KA',
 'Kerala':'KL',
 'Ladakh':'LA',
 'Lakshadweep':'LD',
 'Madhya Pradesh':'MP',
 'Maharashtra':'MH',
 'Manipur':'MN',
 'Meghalaya':'ML',
 'Mizoram':'MZ',
 'Nagaland':'NL',
 'Odisha':'OR',
 'Puducherry':'PY',
 'Punjab':'PB',
 'Rajasthan':'RJ',
 'Sikkim':'SK',
 'Tamil Nadu':'TN',
 'Telangana':'TG',
 'Tripura':'TR',
 'Uttar Pradesh':'UP',
 'Uttarakhand':'UT',
 'West Bengal':'WB'}


# In[31]:


covid = pd.read_csv('districts.csv',header=0)
covid = covid.iloc[1:,:]
# covid = covid[['District_Key','District']]
covid['District'] = covid['District'].str.lower()
covid['State_Code'] = covid['State'].apply(lambda x: statekey[x])
covid = covid[['District','State_Code']]
# covid.head(50)


# In[32]:


# Checking duplicates
# print("Before removing duplicates:")
# print(covid[['District','State_Code']].value_counts())

covid.drop_duplicates(subset =['District','State_Code'],keep = 'first', inplace = True)
# print("After removing duplicates:")
# print(covid[['District','State_Code']].value_counts())


# ## Finding common districts from vaccine and covid datasets

# In[33]:


# x1 = set(vaccine['District'].unique())
# x2 = set(covid['District'].unique())
# common = set(x1.intersection(x2))
# len(common)
y1 = pd.merge(covid,vaccine,on=['District','State_Code'])
# y1


# In[34]:


# y1['District'].value_counts().value_counts()


# # Merging neighbors dataframe with district codes

# In[35]:


df2 = df.copy()
# df2.rename({'District'})
df2 = pd.merge(df2,y1,on='District')
# df2


# In[36]:


df3 = df2.groupby(['District','State_Code','District_Key'])
# df3


# In[37]:


anst = pd.DataFrame()
for x,y in df3:
#     print(x)
#     print(set(y['Neighbors'].values))
    d = {}
    d['District'] = x[0]
    d['State_Code'] = x[1]
    d['District_Key'] = x[2]
    d['Neighbors'] = set(y['Neighbors'].values)
    anst = anst.append(d,ignore_index=True)

anst['Neighbors'] = anst['Neighbors'].apply(lambda x: str(x).replace('{','').replace('}','').replace("'",""))

# anst


# ## Sort on basis of District_Code

# In[38]:


anst.sort_values('District_Key',inplace=True)
anst = anst[['District_Key','Neighbors']]
anst.reset_index(drop=True,inplace=True)


# # Write output to json

# In[39]:


anst.to_json('neighbor-districts-modified.json',orient='records',lines=True)


# In[40]:


print("Execution Completed successfully")


# In[ ]:




