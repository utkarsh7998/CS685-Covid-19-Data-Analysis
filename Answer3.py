#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import pandas as pd
import json
import datetime
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)


# # Reading the csv file

# In[12]:


df = pd.read_csv('districts.csv',parse_dates=['Date'],usecols=['Date','State','District','Confirmed'])
# df


# # Dropping unknown rows and selecting date between 15-03-2021 and 14-08-2021

# In[13]:


df = df[((df['District']!='Unknown') & (df['Date']<='2021-08-14')&(df['Date']>='2020-03-15'))]
df.reset_index(drop=True, inplace=True)
# df


# # Making columns sorted and no. of cases as integer

# In[14]:


df = df.sort_values(['District','Date'])
df['Confirmed'] = df['Confirmed'].astype('int64')
df.reset_index(drop=True, inplace=True)
# df


# # 3.(a) Districtwise Analysis : Weekly

# In[15]:


df1 = df.copy()

df2 =pd.DataFrame(columns=['districtid','weekid','cases','Date']) #weekly

df1 = df1.groupby(['State','District'])
for district, district_df in df1:
#     print(district)
#     print(district_df)
    temp = district_df.shift(1)
    temp.fillna(0,inplace=True)
    district_df['Confirmed'] = district_df['Confirmed'] - temp['Confirmed']
    district_df.set_index('Date',inplace=True)
#     print(district_df)
    t = pd.DataFrame(columns=['districtid','stateid','weekid','cases','Date'])
    t['cases']= district_df.Confirmed.resample('W-Sat').sum()
    t['districtid'] = district[1]
    t['stateid'] = district[0]
    t['Date'] = t.index
    t.reset_index(drop=True,inplace=True)
    t['weekid'] = t.index+1
    t=t[['districtid','stateid','weekid','cases','Date']]
#     print(t)
    df2 = df2.append(t,ignore_index=True)

cases_week = df2.copy()
cases_week = cases_week[['districtid','weekid','cases']]
cases_week['cases'] = cases_week['cases'].astype('int64')
cases_week = cases_week[cases_week['districtid']!='Other State']
cases_week.to_csv('cases-week.csv',index=False)


# In[16]:


# df2


# # 3.(b) Districtwise Analysis: Monthly

# In[17]:



df3 = df.copy()

df4 =pd.DataFrame(columns=['districtid','monthid','cases','Date']) #weekly

df3 = df3.groupby(['State','District'])
for district, district_df in df3:
#     print(district)
#     print(district_df)
    temp = district_df.shift(1)
    temp.fillna(0,inplace=True)
    district_df['Confirmed'] = district_df['Confirmed'] - temp['Confirmed'] # removing cumulative values by shifting
    district_df.rename({'Confirmed':'cases'},axis=1,inplace=True)
    district_df.set_index('Date',inplace=True)
#     print(district_df)
    custom_dates = pd.DatetimeIndex([datetime.date(2020,5,14),
                                     datetime.date(2020,6,14),
                                     datetime.date(2020,7,14),
                                     datetime.date(2020,8,14),
                                     datetime.date(2020,9,14),
                                     datetime.date(2020,10,14),
                                     datetime.date(2020,11,14),
                                     datetime.date(2020,12,14),
                                     datetime.date(2021,1,14),
                                     datetime.date(2021,2,14),
                                     datetime.date(2021,3,14),
                                     datetime.date(2021,4,14),
                                     datetime.date(2021,5,14),
                                     datetime.date(2021,6,14),
                                     datetime.date(2021,7,14),
                                     datetime.date(2021,8,14)])
    t = district_df.groupby(custom_dates[custom_dates.searchsorted(district_df.index)]).sum()

    t['districtid'] = district[1]
    t['stateid'] = district[0]
    t['Date'] = t.index
    t.reset_index(drop=True,inplace=True)
    t['monthid'] = t.index+1
    t=t[['districtid','stateid','monthid','cases','Date']]

#     print(t)
    df4 = df4.append(t,ignore_index=True)


# In[18]:


cases_month = df4.copy()
cases_month = cases_month[['districtid','monthid','cases']]
cases_month['cases'] = cases_month['cases'].astype('int64')
cases_month = cases_month[cases_month['districtid']!='Other State']
cases_month.to_csv('cases-month.csv',index=False)


# # 3.(c) Districtwise Analysis: Overall

# In[19]:


df5 = df.copy()

df6 =pd.DataFrame(columns=['districtid','overallid','cases']) #weekly

df5 = df5.groupby(['State','District'])
for district, district_df in df5:

    temp = district_df.shift(1)
    temp.fillna(0,inplace=True)
    district_df['Confirmed'] = district_df['Confirmed'] - temp['Confirmed']
    district_df.set_index('Date',inplace=True)

    t= {}
    t['cases']= district_df['Confirmed'].sum()
    t['districtid'] = district[1]
    t['stateid'] = district[0]
    t['overallid'] = 1
#     print(t)
    
    df6 = df6.append(t,ignore_index=True)

cases_overall = df6.copy()
cases_overall = cases_overall[['districtid','overallid','cases']]
cases_overall['cases'] = cases_overall['cases'].astype('int64')
cases_overall = cases_overall[cases_overall['districtid']!='Other State']
cases_overall.to_csv('cases-overall.csv',index=False)


# In[20]:


print("Execution completed successfully")


# In[ ]:




