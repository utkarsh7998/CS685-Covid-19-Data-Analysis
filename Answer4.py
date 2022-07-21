#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)


# In[22]:


df = pd.read_csv("districts.csv", parse_dates=['Date'], usecols=['Date','State','District','Confirmed'])
# df


# In[23]:


df = df[((df['District']!='Unknown') & (df['Date'] <= '2021-08-14'))]
df = df.sort_values(['Date','State','District'])
df.reset_index(drop=True, inplace=True)
df['Confirmed'] = df['Confirmed'].astype('int64')
# df.set_index('Date',inplace=True)
# df


# In[24]:


later = pd.DataFrame()


# In[25]:


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


# # District wise Analysis

# In[26]:


import datetime
df1 = df.copy()
# df2 = pd.DataFrame()
ans1 = pd.DataFrame()
df1 = df1.groupby(['State','District'])
for district, district_df in df1:
#     print(district)
    
    
    temp = district_df.shift(1)
    temp.fillna(0,inplace=True)
    district_df['Confirmed'] = district_df['Confirmed'] - temp['Confirmed']
    district_df.set_index('Date',inplace=True)
#     print(district_df)
    later = later.append(district_df)
    
    t1 = pd.DataFrame() #for weeks 1,3,5,...
    t1['cases']= district_df.Confirmed.resample('W-Sun').sum()
    t1['districtid'] = district[1]
    t1['state'] = district[0]
    t1['Date'] = t1.index
    t1.reset_index(drop=True,inplace=True)
#     t1['timeid'] = t1.index+1
#     print(t1)
    
    t2 = pd.DataFrame() #for weeks 2,4,6,8...
    t2['cases']= district_df.Confirmed.resample('W-Thu').sum()
    t2['districtid'] = district[1]
    t2['state'] = district[0]
    t2['Date'] = t2.index
    t2.reset_index(drop=True,inplace=True)
#     t2['timeid'] = t2.index+1
#     print(t2)
    
    t1 = t1.append(t2)
    t1 = t1.sort_values('Date')
    t1.reset_index(drop=True,inplace=True)
    t1['weekid'] = t1.index+1
#     print(t1)
    #peak calculation
    try:
        a = t1.loc[0:40,'cases'].idxmax()
    except:
        a = 27
    try:
        b = t1.loc[100:125,'cases'].idxmax()
    except:
        b = 110
        
    
#     t1.plot(x ='weekid', y='cases', kind = 'line')
#     plt.show()
#     df2 = df2.append(t) #added in weekly dataframe
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
    t3 = district_df.groupby(custom_dates[custom_dates.searchsorted(district_df.index)]).sum()


    t3['districtid'] = district[1]
    t3['state'] = district[0]
    t3['Date'] = t3.index
    t3.reset_index(drop=True,inplace=True)
    t3['monthid'] = t3.index+1
    t3 = t3[['districtid','monthid','Confirmed','Date']]
    t3['Confirmed'] =t3['Confirmed'].astype('int64')
#     print(t3)
#     t3.plot(x ='monthid', y='Confirmed', kind = 'line')
#     plt.show()
    #peak calculation
    try:
        k = t3.loc[1:4,'Confirmed'].idxmax()
    except:
        k = 3
    try:
        l = t3.loc[12:16,'Confirmed'].idxmax()
    except:
        l = 14
        
#     print('weekid: ', a-1, ',',b-1) #printing peak
#     print('monthid: ', k-1,',',l-1) #printing peak
    
    d = {} #dictionary to store district,peak_wave1_weekid,peak_wave2_weekid,peak_wave1_monthid,peak_wave2_monthid
    d['districtid'] = district[1]
    d['state'] = statekey[district[0]]
    d['wave1_weekid'] = a-1
    d['wave2_weekid'] = b-1
    d['wave1_monthid'] = k-1
    d['wave2_monthid'] = l-1
    ans1 = ans1.append(d,ignore_index=True)
    
#     df2 = df2.append(t1)


# In[27]:


ans1['districtid'] = ans1['state']+'_'+ans1['districtid']


# In[28]:


ans1['wave1_weekid'] = ans1['wave1_weekid'].astype('int')
ans1['wave2_weekid'] = ans1['wave2_weekid'].astype('int')
ans1['wave1_monthid'] = ans1['wave1_monthid'].astype('int')
ans1['wave2_monthid'] = ans1['wave2_monthid'].astype('int')
ans1_new = ans1[['districtid','wave1_weekid','wave2_weekid','wave1_monthid','wave2_monthid']]
ans1_new = ans1_new[ans1_new['districtid']!='Other State']
ans1_new


# In[29]:


ans1_new.to_csv('district-peaks.csv',index=False)


# # Statewise Analysis

# In[30]:



df3 = later.copy()
df3['Date'] = df3.index
df3.reset_index(drop=True, inplace=True)
# df3


# In[31]:


df5 = df3.copy()
df6 = pd.DataFrame()
# df5['Date'] = pd.to_datetime(df5['Date'])
df5 = df5.groupby(['State','Date'])
for district, district_df in df5:
#     print(district[1].date())
#     print(district_df)
    d = {}
    d['stateid'] = district[0]
    d['Date'] = str(district[1].date())
    d['Confirmed'] = district_df['Confirmed'].sum()
#     print(d)
    df6 = df6.append(d,ignore_index=True)


# In[32]:


# df6 #contains statewise daily data


# In[33]:


df7 = df6.groupby('stateid')
# df7


# In[34]:


ans2 = pd.DataFrame()
for district, district_df in df7:
#     print(district)
#     print(district_df)
    district_df['Date'] = pd.to_datetime(district_df['Date'])
    district_df.set_index('Date',inplace=True)
#     print(district_df)
    
##########    WEEKLY ESTIMATION ###########################################
    t1 = pd.DataFrame() #for weeks 1,3,5,...
    t1['cases']= district_df.Confirmed.resample('W-Sun').sum()
#     t1['districtid'] = district[1]
    t1['state'] = district
    t1['Date'] = t1.index
    t1.reset_index(drop=True,inplace=True)
#     t1['timeid'] = t1.index+1
#     print(t1)
    
    t2 = pd.DataFrame() #for weeks 2,4,6,8...
    t2['cases']= district_df.Confirmed.resample('W-Thu').sum()
#     t2['districtid'] = district[1]
    t2['state'] = district
    t2['Date'] = t2.index
    t2.reset_index(drop=True,inplace=True)
#     t2['timeid'] = t2.index+1
#     print(t2)
    
    t1 = t1.append(t2)
    t1 = t1.sort_values('Date')
    t1.reset_index(drop=True,inplace=True)
    t1['weekid'] = t1.index+1
#     print(t1)
    #peak calculation
    try:
        a = t1.loc[0:40,'cases'].idxmax()
    except:
        a = 15
    if (a==0):
        a=15
    try:
        b = t1.loc[100:125,'cases'].idxmax()
    except:
        b = 110
        
    
#     t1.plot(x ='weekid', y='cases', kind = 'line')
#     plt.show()
##########    MONTHLY ESTIMATION ###########################################
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
    t3 = district_df.groupby(custom_dates[custom_dates.searchsorted(district_df.index)]).sum()


#     t3['districtid'] = district[1]
    t3['state'] = district
    t3['Date'] = t3.index
    t3.reset_index(drop=True,inplace=True)
    t3['monthid'] = t3.index+1
    t3 = t3[['state','monthid','Confirmed','Date']]
    t3['Confirmed'] =t3['Confirmed'].astype('int64')
#     print(t3)
#     t3.plot(x ='monthid', y='Confirmed', kind = 'line')
#     plt.show()
    #peak calculation
    try:
        k = t3.loc[1:4,'Confirmed'].idxmax()
    except:
        k = 3

    try:
        l = t3.loc[12:16,'Confirmed'].idxmax()
    except:
        l = 14
    
#     print('weekid: ', a-1, ',',b-1) #printing peak
#     print('monthid: ', k-1,',',l-1) #printing peak
    
    d = {} #dictionary to store district,peak_wave1_weekid,peak_wave2_weekid,peak_wave1_monthid,peak_wave2_monthid
#     d['districtid'] = district[1]
    d['state'] = district
    d['wave1_weekid'] = a-1
    d['wave2_weekid'] = b-1
    d['wave1_monthid'] = k-1
    d['wave2_monthid'] = l-1
    ans2 = ans2.append(d,ignore_index=True)
    
#     df2 = df2.append(t1)


# In[35]:


ans2['wave1_monthid'] = ans2['wave1_monthid'].astype('int')
ans2['wave2_monthid'] = ans2['wave2_monthid'].astype('int')
ans2['wave1_weekid'] = ans2['wave1_weekid'].astype('int')
ans2['wave2_weekid'] = ans2['wave2_weekid'].astype('int')
ans2 = ans2[['state','wave1_weekid','wave2_weekid','wave1_monthid','wave2_monthid']]
# ans2


# In[36]:


ans2.to_csv('state-peaks.csv',index=False)


# # Overall Analysis

# In[37]:


df8 = later.copy()
df8['Date'] = df8.index
df8.reset_index(drop=True,inplace=True)
df8.drop(['State','District'],axis=1,inplace=True)
df8 = pd.DataFrame(df8.groupby('Date')['Confirmed'].sum())
df8['Date'] = df8.index
df8.reset_index(drop=True,inplace=True)
df8.set_index('Date',inplace=True)
# df8


# In[38]:


def fun(district_df):
    ans3 = pd.DataFrame()
    
    t1 = pd.DataFrame() #for weeks 1,3,5,7...
    t1['cases']= district_df.Confirmed.resample('W-Sun').sum()
    t1['Date'] = t1.index
    t1.reset_index(drop=True,inplace=True)
#     print(t1)
    
    t2 = pd.DataFrame() #for weeks 2,4,6,8...
    t2['cases']= district_df.Confirmed.resample('W-Thu').sum()
    t2['Date'] = t2.index
    t2.reset_index(drop=True,inplace=True)
#     print(t2)
    
    t1 = t1.append(t2)
    t1 = t1.sort_values('Date')
    t1.reset_index(drop=True,inplace=True)
    t1['weekid'] = t1.index+1
#     print(t1)
    
#     peak estimation 
    try:
        a = t1.loc[0:60,'cases'].idxmax() #Wave1 peak
    except:
        a = 30 
    
    if (a==0):
        a=30
    
    try:
        b = t1.loc[90:120,'cases'].idxmax() #Wave2 peak
    except:
        b = 110

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
    t3 = district_df.groupby(custom_dates[custom_dates.searchsorted(district_df.index)]).sum()

    t3['Date'] = t3.index
    t3.reset_index(drop=True,inplace=True)
    t3['monthid'] = t3.index+1
    t3 = t3[['monthid','Confirmed','Date']]
    t3['Confirmed'] =t3['Confirmed'].astype('int64')

    #peak calculation
    try:
        k = int(t3.loc[1:4,'Confirmed'].idxmax())
    except:
        k = 3

    try:
        l = int(t3.loc[12:16,'Confirmed'].idxmax())
    except:
        l = 14
    
    
    d = {} #dictionary to store district,peak_wave1_weekid,peak_wave2_weekid,peak_wave1_monthid,peak_wave2_monthid

    d['overallid'] = 'India'
    d['wave1_weekid'] = str(--a)
    d['wave2_weekid'] = str(--b) 
    d['wave1_monthid'] = str(--k)
    d['wave2_monthid'] = str(--l)
#     print(a,b,k,l)
    
    ans3 = ans3.append(d,ignore_index=True)
    ans3 = ans3[['overallid','wave1_weekid','wave2_weekid','wave1_monthid','wave2_monthid']]
    
    ans4 = ans3.copy()
#     print(ans4)
    
    ans4.to_csv('overall-peaks.csv',index=False)
    
#     df2 = df2.append(t1)


# In[39]:


fun(df8.copy())


# In[40]:


print("Execution Completed successfully")


# In[ ]:




