#!/usr/bin/env python
# coding: utf-8

# In[187]:


import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)


# In[188]:


#**Accomodation**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['#Accomodation']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name,tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[189]:


#**Accomodation**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['#crime']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name,tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[190]:


#**Rent**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['#rent']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name,tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[191]:


#**Transportation**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['#transportation']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[192]:


#**Propertrymgmt**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['@UnitedRentals']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[193]:


#**SocialIssues**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['#housingisahumanright']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[194]:


#**Entertainment**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['theatre','park']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location,tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[195]:


#**Crimes**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['crime']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[196]:


#**Educational**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['#student']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[197]:


#**Health**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['hospital']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[198]:


#**Sports**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['sport']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[199]:


#**Job**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['job']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[185]:


#**Weather**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['weather']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[200]:


#**Food**
import tweepy
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import re
api_key = "oxGYavm8tOZZ9J0qiNFXOkAPR"
api_key_secret = "OVHYddylqsHt0uQ3HMcNru9g8dgpkyoZPG2yrcj3UyPcD4CazJ"
access_token = "1590488748432629760-OtUoEpW5RyHN4S3AuMyGNV5M99mZre"
access_token_secret = "vFg0k8FF5avKh55m95PloXdxF4h10plx59Yaig2ZM5k3y"

#authentication

auth = tweepy.OAuth1UserHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

keywords = ['food']

limit = 300

#tweepy.Cursor()

tweets = tweepy.Cursor(api.search_tweets,q=keywords, count = 100, tweet_mode='extended').items(limit)
tweet_columns = ['tweet_id','Twitter_handle','tweet_text', 'country','city','retweet_count','favorite_count','created_at']
tweet_data = []
user_columns = ['Twitter_handle','name','description','followers_count','following_count','location','created_at']
user_data=[]
mention_columns=['tweet_id','source_user','target_user']
mention_data=[]
tag_columns=['tweet_id','tweet_tags']
tag_data=[]

users=[]
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        sql = "select Twitter_handle from tweets"
        cursor.execute(sql)
        r = cursor.fetchone()
        while r is not None:
            users.append(r[0])
            r = cursor.fetchone()
            
    #print (users)
    cursor.close()
    conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    cursor.close()
    conn.close()
        
for tweet in tweets:
    
    if tweet.place == None:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],"NA","NA",tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    else:
        tweet_data.append([tweet.id_str,tweet.user.screen_name,tweet.full_text[1:450],tweet.place.country,tweet.place.name[0:18],tweet.retweet_count,tweet.favorite_count,tweet.created_at])
    if tweet.user.screen_name not in users:
        user_data.append([tweet.user.screen_name,tweet.user.name,tweet.user.description,tweet.user.followers_count,tweet.user.friends_count,tweet.user.location[0:18],tweet.user.created_at])
    tmentions = re.findall("@([a-zA-Z0-9_]{1,50})", tweet.full_text)
    thashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet.full_text)
    if len(tmentions) !=0:
        men=""
        j=0
        for i in tmentions:
            if j==0:
                men=i
                
            else:
                men=men+","+i
        mention_data.append([tweet.id_str,tweet.user.screen_name,men])
    if len(thashtags)!=0:
        tag=""
        j=0
        for i in thashtags:
            if j==0:
                tag=i;
                
            else:
                tag=tag+","+i
        tag_columns.append([tweet.id_str,tag])        
        

df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns)
df_user = pd.DataFrame(user_data, columns= user_columns)
df_mention = pd.DataFrame(mention_data, columns= mention_columns)
df_tag = pd.DataFrame(tag_data, columns= tag_columns)


df_user.drop_duplicates(subset=['Twitter_handle'])
df_tweet['created_at'] = df_tweet['created_at'].apply(lambda a: pd.to_datetime(a))
df_user['created_at'] = df_user['created_at'].apply(lambda a: pd.to_datetime(a))

try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        cursor = conn.cursor()
        
        #insert data into tweets
        for i,row in df_tweet.iterrows():
            sql = "INSERT INTO Tweets(tweet_id,Twitter_handle,tweet_text,country,city,retweet_count,favorite_count,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
        
        
        #insert data into user
        for i,row in df_user.iterrows():
            sql = "INSERT INTO User(Twitter_handle,name,description,followers_count,following_count,location,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_mention.iterrows():
            sql = "INSERT INTO Tweet_Mentions(tweet_id,source_user,target_user) VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        #insert data into user
        for i,row in df_tag.iterrows():
            sql = "INSERT INTO Tags(tweet_id,tweet_tags) VALUES (%s,%s)"
            cursor.execute(sql, tuple(row))
            #print("Record inserted")
            conn.commit()
            
        cursor.close()
        conn.close()
except Error as e:
            print("Error while connecting to MySQL", e)
            if cursor and conn:
                cursor.close()
                conn.close() 


# In[162]:


if cursor and conn:
                cursor.close()
                conn.close() 


# #**Twitter question1 : Which user posted this tweet?** 

# select twitter_handle,tweet_text tweet from Tweets where Twitter_handle='theluckyman';

# In[154]:


#For All users
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        #print(1)
        cursor = conn.cursor()
        sql = "select twitter_handle,tweet_text tweet from Tweets"
        #print(3)
        cursor.execute(sql)
        #print(4)
        r = cursor.fetchone()
        tweet_columns = ['User','Tweet']
        tweet_data = []
        while r is not None:
            #print(r)
            tweet_data.append(list(r))
            r = cursor.fetchone()
            
        df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns) 
        display(df_tweet)
        cursor.close()
        conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    #print(2)
    if cursor and conn:
        #cursor.close()
        conn.close()


# #**Twitter question2 : When did the user post this tweet?**

# select twitter_handle,tweet_text,created_at tweet from Tweets  where Twitter_handle='theluckyman';

# In[155]:


#For All users
try:
    conn = msql.connect(host='localhost', database='rentalbuddy', user='root', password='amey@1105',auth_plugin='mysql_native_password')
    if conn.is_connected():
        #print(1)
        cursor = conn.cursor()
        sql = "select twitter_handle,tweet_text,created_at tweet from Tweets"
        #print(3)
        cursor.execute(sql)
        #print(4)
        r = cursor.fetchone()
        tweet_columns = ['User','Tweet','Tweet Posted Date']
        tweet_data = []
        while r is not None:
            #print(r)
            tweet_data.append(list(r))
            r = cursor.fetchone()
            
        df_tweet = pd.DataFrame(tweet_data, columns= tweet_columns) 
        display(df_tweet)
        cursor.close()
        conn.close()
except Error as e:
    print("Error while connecting to MySQL", e)
    #print(2)
    if cursor and conn:
        #cursor.close()
        conn.close()


# #**Twitter question3: What tweets have this user posted in the past 24 hours?** 

# select Twitter_handle, tweet_text, created_at from rentalbuddy.tweets 
# where  created_at < SYSDATE() 
# and created_at > DATE_SUB(SYSDATE() , INTERVAL 1 DAY ) and Twitter_handle= <input username> ;

# #**Twitter question4: How many tweets have this user posted in the past 24 hours?** 

# select count(*) No_of_tweets ,Twitter_handle from rentalbuddy.tweets 
# where  created_at >SYSDATE() 
# and created_at > DATE_SUB(SYSDATE() , INTERVAL 1 DAY ) and Twitter_handle='theluckyman'group by Twitter_handle order by count(*) desc;

# #**Twitter question5: When did this user join Twitter?** 

# select Twitter_handle,name,created_at from user where Twitter_handle='theluckyman';

# #**Twitter question6: What keywords/ hashtags are popular?** 
# 

#  select count(*),target_user from rentalbuddy.Tweet_Mentions  group by target_user order by count(*) desc;

# #**Twitter question7: What tweets are popular?** 

# In[ ]:


select Twitter_handle,retweet_count, tweet_text from rentalbuddy.tweets   order by retweet_count desc limit 1;


# In[ ]:





# In[ ]:




