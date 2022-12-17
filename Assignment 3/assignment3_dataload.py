#!/usr/bin/env python
# coding: utf-8

# In[31]:


import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
df_apt = pd.read_csv(r'C:\Users\amey8\Downloads\Assignment3\JuneApt.csv')
df_amenities = pd.read_csv(r'C:\Users\amey8\Downloads\Assignment3\JuneAmenities.csv')
df_transport = pd.read_csv(r'C:\Users\amey8\Downloads\Assignment3\Transport.csv')
try:
    
    conn = msql.connect(host='localhost', database='rental_buddydb', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    
    if conn.is_connected():
        cursor = conn.cursor()
        
        for i,row in df_apt.iterrows():
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
            
        for i,row in df_amenities.iterrows():
            t=[]
            i=0
            for j in row:
                if(i!=0):
                    t.append(j)
                i=i+1
            sql = "INSERT INTO JuneAmenitites(id,Amenities) VALUES (%s,%s)"
            #print(sql)
            cursor.execute(sql, tuple(t))
            conn.commit()
            
        for i,row in df_transport.iterrows():
            t=[]
            i=0
            for j in row:
                if(i!=0):
                    t.append(j)
                i=i+1
            sql = "INSERT INTO Junetransport(id,Trans_id,stations,color,walktime,description) VALUES (%s,%s,%s,%s,%s,%s)"
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


# In[ ]:





# In[ ]:




