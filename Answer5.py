#!/usr/bin/env python
# coding: utf-8

# In[63]:


import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[64]:


df = pd.read_csv('cowin_vaccine_data_districtwise.csv',low_memory=False)
df = df[1:]
df.reset_index(drop=True, inplace=True)
df.fillna(0,inplace=True)
# df


# In[65]:


selected_dates = pd.date_range(start ='16-01-2021',end ='14-08-2021', freq ='D')
cols = [d.strftime('%d/%m/%Y') for d in selected_dates]


# In[66]:


ans = []


# In[67]:


for j in range(len(cols)):
    for i in range(len(df)):
        tmp = {}
        tmp['Date'] = cols[j]
        tmp['State_Code'] = df.loc[i, 'State_Code']
        tmp['District_Key'] = df.loc[i, 'District_Key']
        tmp['Dose1'] = df.loc[i,cols[j]+'.3']
        tmp['Dose2'] = df.loc[i,cols[j]+'.4']
        ans.append(tmp)
#     print(j)


# In[68]:


df = pd.DataFrame(ans)
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Dose1'] = df['Dose1'].astype('int64')
df['Dose2'] = df['Dose2'].astype('int64')
# df


# # Since there are multiple rows with same district_keys, therefore adding them by using Group by and sum command

# In[69]:


df = df.groupby(['Date','District_Key'])['Dose1','Dose2'].sum()
# df


# In[70]:


df['Date'] = df.index.to_numpy()
df['District_Key'] = df.index.to_numpy()
df['Date'] = df['Date'].apply(lambda x: x[0])
df['District_Key'] = df['District_Key'].apply(lambda x:x[1])
df.reset_index(drop=True,inplace=True)
# df


# In[71]:


df= df[['Date','District_Key','Dose1','Dose2']]
df.sort_values(['District_Key','Date'],inplace=True)
df.reset_index(drop=True, inplace=True)
# df


# # 1.District Wise Analysis

# ##                            i) District: Weekly Analysis

# In[72]:


df1 = df.copy()

df2 =pd.DataFrame(columns=['districtid','weekid','dose1','dose2','Date']) #weekly

df1 = df1.groupby('District_Key')
for district, district_df in df1:
#     print(district)
#     print(district_df)
    temp = district_df.shift(1)
    temp.fillna(0,inplace=True)
    district_df['Dose1'] = district_df['Dose1'] - temp['Dose1']
    district_df['Dose2'] = district_df['Dose2'] - temp['Dose2']
    district_df.set_index('Date',inplace=True)
#     print(district_df)
    t = pd.DataFrame(columns=['districtid','weekid','dose1','dose2','Date'])
    t['dose1']= district_df.Dose1.resample('W-Sat').sum().astype('int64')
    t['dose2']= district_df.Dose2.resample('W-Sat').sum().astype('int64')
    t['districtid'] = district
    t['Date'] = t.index
    t.reset_index(drop=True,inplace=True)
    t['weekid'] = t.index+1
    t=t[['districtid','weekid','dose1','dose2','Date']]

#     print(t)
    df2 = df2.append(t,ignore_index=True)


# In[73]:


# df2
ans1 = df2[['districtid','weekid','dose1','dose2']]


# In[74]:


# Writing output to file
ans1.to_csv('district-vaccinated-count-week.csv',index=False)


# ## ii) District: Monthly analysis

# In[75]:


import datetime
df3 = df.copy()
df3.set_index('Date',inplace=True)
df4 = pd.DataFrame()


df3 = df3.groupby(['District_Key'])
for district, district_df in df3:

    temp = district_df.shift(1)
    temp.fillna(0,inplace=True)
    district_df['Dose1'] = district_df['Dose1'] - temp['Dose1']
    district_df['Dose2'] = district_df['Dose2'] - temp['Dose2']
    

    custom_dates = pd.DatetimeIndex([datetime.date(2021,2,14),
                                     datetime.date(2021,3,14),
                                     datetime.date(2021,4,14),
                                     datetime.date(2021,5,14),
                                     datetime.date(2021,6,14),
                                     datetime.date(2021,7,14),
                                     datetime.date(2021,8,14)])
    t1 = district_df.groupby(custom_dates[custom_dates.searchsorted(district_df.index)]).sum()

    t1['districtid'] = district
    t1['Date'] = t1.index
    t1.reset_index(drop=True,inplace=True)
    t1['monthid'] = t1.index+1
    t1 = t1 [['districtid','monthid','Dose1','Dose2','Date']]
    t1['Dose1'] =t1['Dose1'].astype(int)
    t1['Dose2'] =t1['Dose2'].astype(int)
#     print(t1)
    df4 = df4.append(t1)


# In[76]:


ans2 = df4[['districtid','monthid','Dose1','Dose2']]
# df4.head(10)


# In[77]:


# Writing output to file
ans2.to_csv('district-vaccinated-count-month.csv',index=False)


# ## iii) District: Overall analysis

# In[78]:


df5 = df2.copy()
df6 = pd.DataFrame()
df5 = df5.groupby('districtid')
# df2 = pd.DataFrame()
for districtid, dataframe in df5:
#     print(districtid)
#     print(dataframe)
    t = {}
    t['districtid'] = districtid
    t['overallid'] = str(1)
    t['dose1'] = dataframe['dose1'].sum()
    t['dose2'] = dataframe['dose2'].sum()
#     print(t)
    df6 = df6.append(t,ignore_index=True)


# In[79]:


# df6
ans3 = df6[['districtid','overallid','dose1','dose2']]
ans3['dose1'] = ans3['dose1'].astype(int)
ans3['dose2'] = ans3['dose2'].astype(int)


# In[80]:


# Writing output to file
ans3.to_csv('district-vaccinated-count-overall.csv',index=False)


# # Statewise Analysis

# ## i) Statewise: Weekly Analysis

# In[81]:


#Using old dataframe created in District: Week Analysis.

df7 = df2.copy() 
df7['stateid'] = df7['districtid'].apply(lambda x: x.split('_')[0])
df7.drop(['Date','districtid'],axis=1,inplace=True)
df7 = df7.groupby(['weekid','stateid'])['dose1','dose2'].sum()
df7['weekid'] = df7.index.to_numpy()
df7['stateid'] = df7.index.to_numpy()
df7['weekid'] = df7['weekid'].apply(lambda x: x[0])
df7['stateid'] = df7['stateid'].apply(lambda x:x[1])
df7.reset_index(drop=True,inplace=True)
df7 = df7.sort_values(['stateid','weekid'])
df7=df7[['stateid','weekid','dose1','dose2']]
df7.reset_index(drop=True,inplace=True)

# df7


# In[82]:


# Writing output to file
ans4 = df7.copy()
ans4.to_csv('state-vaccinated-count-week.csv',index=False)


# # ii) Statewise: monthly analysis

# In[83]:


df8 = df4.copy()
df8 = df8.groupby(['districtid','monthid'])['Dose1','Dose2'].sum()
df8['stateid'] = df8.index
df8['monthid'] = df8.index
df8.reset_index(drop=True,inplace=True)
df8['stateid'] = df8['stateid'].apply(lambda x: x[0])
df8['monthid'] = df8['monthid'].apply(lambda x: x[1])
df8 = df8[['stateid','monthid','Dose1','Dose2']]
df8['Dose2'] = df8['Dose2'].astype('int64')
# df8


# In[84]:


# Writing output to file
ans5 = df8.copy()
ans5.to_csv('state-vaccinated-count-month.csv',index=False)


# # iii) Statewise: Overall analysis

# In[85]:


df9 = df4.copy()
df9['stateid'] = df9['districtid'].apply(lambda x: x.split('_')[0])
df9 = df9.drop(['districtid','Date','monthid'],axis=1)
df9 = df9.groupby('stateid')['Dose1','Dose2'].sum()
df9['stateid'] = df9.index.to_numpy()
df9['overallid'] = str(1)
df9.reset_index(drop=True,inplace=True)
df9 = df9[['stateid','overallid','Dose1','Dose2']]
# df9


# In[86]:


# Writing output to file
ans6 = df9.copy()
ans6.to_csv('state-vaccinated-count-overall.csv',index=False)


# In[87]:


print("Execution completed successfully")


# In[ ]:




