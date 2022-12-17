-- 1
select twitter_handle,tweet_text tweet from Tweets where Twitter_handle='theluckyman';
-- 2
select twitter_handle,tweet_text,created_at tweet from Tweets  where Twitter_handle='theluckyman';

-- 3
select Twitter_handle, tweet_text, created_at from rentalbuddy.tweets 
where  created_at >SYSDATE() 
and created_at > DATE_SUB(SYSDATE() , INTERVAL 1 DAY ) and Twitter_handle='theluckyman';

-- 4
select count(*) No_of_tweets ,Twitter_handle from rentalbuddy.tweets 
where  created_at <SYSDATE() 
and created_at > DATE_SUB(SYSDATE() , INTERVAL 1 DAY ) and Twitter_handle='theluckyman'group by Twitter_handle order by count(*) desc;

-- 5
select Twitter_handle,name,created_at from user where Twitter_handle='theluckyman';

-- 6
 select count(*),target_user from rentalbuddy.Tweet_Mentions  group by target_user order by count(*) desc;

-- 7
select Twitter_handle,retweet_count, tweet_text from rentalbuddy.tweets   order by retweet_count desc limit 1;


-- extras
select Twitter_handle,max(No_of_tweets) from (select count(*) No_of_tweets ,Twitter_handle from rentalbuddy.tweets 
where  created_at >SYSDATE() 
and created_at > DATE_SUB(SYSDATE() , INTERVAL 1 DAY ) group by Twitter_handle order by count(*) desc) as a  ;


select * from rentalbuddy.tweets where  created_at >SYSDATE() 
and created_at > DATE_SUB(SYSDATE() , INTERVAL 1 DAY );

select Twitter_handle,retweet_count, tweet_text from rentalbuddy.tweets order by retweet_count desc;

select DATE_SUB(SYSDATE() , INTERVAL 1 DAY );