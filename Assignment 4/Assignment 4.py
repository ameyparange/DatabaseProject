#!/usr/bin/env python
# coding: utf-8

# In[22]:


import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re


# In[29]:


Juneapt=[]
try:
    conn = msql.connect(host='localhost', database='rental_buddydb', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select * from juneapartments"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            Juneapt.append(r)
            r = cursor.fetchone()
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()


# In[30]:


df_apt = pd.DataFrame (Juneapt, columns= ['id','Apt_id','url','Address','Beds','Bath','Price','BedArea','Availablefrom','Availabletill','Description'])


# In[31]:


df_apt


# In[33]:


address=[]
Juneapt_1nf=[]
for apt in Juneapt:
    address=apt[3].split('/')
    for add in address:
        t=[apt[0],apt[1],apt[2],add,apt[4],apt[5],apt[6],apt[7],apt[8],apt[9],apt[10]]
        Juneapt_1nf.append(t)


# In[34]:


df_apt_1nf = pd.DataFrame (Juneapt_1nf, columns= ['did','Apt_id','url','Address','Beds','Bath','Price','BedArea','Availablefrom','Availabletill','Description'])


# In[35]:


df_apt_1nf.normaliz


# ##*2 NF*

# In[36]:


import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re

try:
    
    conn = msql.connect(host='localhost', database='rental_buddydb', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    
    if conn.is_connected():
        cursor = conn.cursor()
        
        for i,row in df_apt_1nf.iterrows():
            t=[]
            i=0
            for j in row:
                if(i!=0):
                    t.append(j)
                i=i+1
            sql = "INSERT INTO JuneApartments(id,Apt_id,url,Address,Beds,Bath,Price,BedArea,Availablefrom,Availabletill,Description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #print(sql)
            cursor.execute(sql, tuple(t))
            conn.commit()
            
        
            
        cursor.close()
        conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    if cursor and conn:
        cursor.close()
        conn.close() 

