import tweepy
import csv
import json
from pymongo import MongoClient

client = MongoClient()


#Twitter API credentials
consumer_key = "IIJVagCrIuipiZQRNxiX8okOO"
consumer_secret = "TwigYDzho9YGUOlGIPvNQJXhZt0aY5r33YbaA6ijifPKN0JvPr"
access_key = "1298538012-Td1042ReUAagHzSDDPlCa9eOpbJmwc6uB3BmYOd"
access_secret = "qufnJEjTDgXTicuyl3vsAbipHYAoDYUhJOKtmrr9p6w5i"


def get_all_tweets(screen_name):
    t_db = client[screen_name+'_db']
    t_colle = t_db[screen_name+'_collection']
    posts = t_db['posts']
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab

    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
    
    #transform the tweepy tweets into a 2D array that will populate the csv 

    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.coordinates, tweet.geo, tweet.place] for tweet in alltweets]

    for tweet in alltweets:
        post_id = posts.insert_one({'id_str':tweet.id_str,'created_at':tweet.created_at, 'text':tweet.text.encode("utf-8"), 'coordinates':tweet.coordinates, 'geo':tweet.geo})
        print post_id
    #write the csv  
    """
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    """
    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("ponguru")
    get_all_tweets("thekiranbedi")
