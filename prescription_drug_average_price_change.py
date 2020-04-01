#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime  
from datetime import date, timedelta 
import calendar 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df1=pd.read_csv('NADAC__National_Average_Drug_Acquisition_Cost_.csv')


# In[3]:


df1.head()


# In[4]:


df1.dtypes


# In[5]:


df1['NDC']=df1['NDC'].astype('str')
df1.dtypes


# In[6]:


df2=df1.dropna(subset = ["Corresponding_Generic_Drug_NADAC_Per_Unit"])


# In[7]:


df2.head()


# In[8]:


df2.shape


# In[9]:


df_price=df1[['NDC Description','NDC','NADAC_Per_Unit','Effective_Date','OTC','Classification_for_Rate_Setting']]


# In[10]:


df_price = df_price.drop_duplicates()


# In[11]:


df_price.head()


# In[12]:


df_price['NDC'].unique().size


# In[13]:


df_price['NDC Description'].unique().size


# In[14]:


df_price[df_price['NDC Description']=='ENEMA']


# In[15]:


df_price.sort_values(by=['NDC'])


# In[16]:


df_price['NDC']=df_price['NDC'].apply('{:0>11}'.format)


# In[17]:


df_price.head()


# In[18]:


def findDay(date): 
    month, day, year = (int(i) for i in date.split('/'))     
    born = datetime.date(year, month, day) 
    return born.strftime("%A")


# In[19]:


df_price['Effective_Date'].apply(findDay)


# In[20]:


def wednesday(date): 
    month, day, year = (int(i) for i in date.split('/'))     
    born = datetime.date(year, month, day) 
    t=born.weekday()
    newdate=born-timedelta(days=t-2)
    return newdate


# In[21]:


wednesday(df_price.loc[3,'Effective_Date'])


# In[22]:


date=df_price.loc[3,'Effective_Date']


# In[23]:


month, day, year = (int(i) for i in date.split('/'))     
born = datetime.date(year, month, day) 
t=born.weekday()
t


# In[24]:


df_price['date']=df_price['Effective_Date'].apply(wednesday)


# In[25]:


df_price.head()


# In[26]:


df_price['NADAC_Per_Unit']=df_price.groupby(['NDC','date'])['NADAC_Per_Unit'].transform('mean')


# In[27]:


df_price.drop(['Effective_Date'],axis=1,inplace=True)


# In[28]:


df_price[['NDC','date']].shape


# In[29]:


df_price.drop_duplicates(subset=['date','NDC'],keep=False, inplace=True)
df_price.shape


# In[30]:


x=df_price['date'].unique()
x.sort()


# In[31]:


x


# In[32]:


mux = pd.MultiIndex.from_product([df_price['NDC'].unique(), 
                                  df_price['date'].unique()],
                                  names=['NDC','date'])


# In[33]:


df_balanced =  df_price.set_index(['NDC','date']).reindex(mux).reset_index()


# In[34]:


df_balanced[df_balanced['NDC']==df_balanced['NDC'][0]].sort_values(by=['date'],ascending=True)


# In[35]:


df_balanced['NDC']=df_balanced['NDC'].astype('str')


# In[36]:


df_balanced=df_balanced.sort_values(by=['NDC','date'])
df_balanced.head()


# In[37]:


df_balanced['NADAC_Per_Unit']=df_balanced.groupby('NDC')['NADAC_Per_Unit'].apply(lambda x: x.ffill())


# In[38]:


df_balanced['NDC Description']=df_balanced.groupby('NDC')['NDC Description'].apply(lambda x: x.fillna(x.mode()[0]))


# In[39]:


df_balanced['OTC']=df_balanced.groupby('NDC')['OTC'].apply(lambda x: x.fillna(x.mode()[0]))


# In[40]:


df_balanced['Classification_for_Rate_Setting']=df_balanced.groupby('NDC')['Classification_for_Rate_Setting'].apply(lambda x: x.fillna(x.mode()[0]))


# In[41]:


df_balanced.head()


# In[42]:


temp=df_balanced.loc[df_balanced['date']=='2014-01-01']
temp_list=temp[temp['NADAC_Per_Unit'].isnull()]['NDC']
temp_list


# In[43]:


df_balanced['NDC'].unique().size


# In[44]:


df_plot=df_balanced.loc[~df_balanced['NDC'].isin(temp_list)]


# In[45]:


df_plot=df_plot[df_plot['date']>='2014-1-1']


# In[46]:


df_plot.head()


# In[47]:


df_plot['Price_Level']=df_plot['NADAC_Per_Unit']/df_plot.groupby('NDC')['NADAC_Per_Unit'].transform('first')


# In[48]:


df_plot.head()


# In[49]:


df_pre=df_plot[df_plot['OTC']=='N'].reset_index()


# In[50]:


df_total=pd.DataFrame(df_plot['date'].drop_duplicates()).reset_index()


# In[51]:


df_total.sort_values('date')


# In[52]:


df_total['All_Drugs']=df_pre.groupby('date')['Price_Level'].mean().values
df_total['Brand_Drugs']=df_pre[df_pre['Classification_for_Rate_Setting']=='B'].groupby('date')['Price_Level'].mean().values
df_total['Generic_Drugs']=df_pre[df_pre['Classification_for_Rate_Setting']=='G'].groupby('date')['Price_Level'].mean().values
df_total['ANDA_Drugs']=df_pre[df_pre['Classification_for_Rate_Setting']=='B-ANDA'].groupby('date')['Price_Level'].mean().values


# In[53]:


df_total.head()


# In[54]:


df_total.drop(['index'], axis=1)


# In[55]:


plt.plot(df_total['date'],df_total['All_Drugs'], label="All Drugs")
plt.plot(df_total['date'],df_total['Brand_Drugs'], label="Brand Drugs")
plt.plot(df_total['date'],df_total['Generic_Drugs'], label="Generic Drugs")
#plt.plot(df_total['date'],df_total['ANDA_Drugs'], label="ANDA Drugs")
# Add legend
plt.legend(loc='upper left')
# Add title and x, y labels
plt.title("Price Change of Prescription Drugs", fontsize=16, fontweight='bold')
#plt.suptitle("Random Walk Suptitle", fontsize=10)
plt.xlabel("Time")
plt.ylabel("Price Level")
plt.show()


# In[56]:


plt.savefig('Price Change of Prescription Drugs.png')


# In[ ]:





# In[57]:


df_price_change=df_plot[(df_plot['OTC']=='N')&(df_plot['date']=='2020-03-25')].reset_index()
df_price_change.head()


# In[58]:


df_price_change.drop(['date','index'],axis=1)


# In[59]:


import seaborn as sns


# In[60]:


sns.boxplot(y='Price_Level', x='Classification_for_Rate_Setting', 
                 data=df_price_change[df_price_change['Classification_for_Rate_Setting']!='B-ANDA'])


# In[61]:


df_price_change.sort_values(by=['Price_Level'],inplace=True)


# In[62]:


sns.boxplot(y='Price_Level', x='Classification_for_Rate_Setting', 
                 data=df_price_change[df_price_change['Classification_for_Rate_Setting']!='B-ANDA'].iloc[:-100]).set_title('Distributions of Price Changes For Generic Drugs and Brand-Name Drugs')


# In[63]:


plt.savefig('Distributions of Price Changes.png')

