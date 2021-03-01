# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:13:52 2021

@author: iremdogan
"""


'''
What to get over status in on_status func.

The user’s description (status.user.description). This is the description the user who created the tweet wrote in their biography.
The user’s location (status.user.location). This is the location the user who created the tweet wrote in their biography.
The screen name of the user (status.user.screen_name).
When the user’s account was created (status.user.created_at).
How many followers the user has (status.user.followers_count).
The background color the user has chosen for their profile (status.user.profile_background_color).
The text of the tweet (status.text).
The unique id that Twitter assigned to the tweet (status.id_str).
When the tweet was sent (status.created_at).
How many times the tweet has been retweeted (status.retweet_count).
The tweet’s coordinates (status.coordinates). The geographic coordinates from where the tweet was sent.

'''    


import tweepy
from tweepy import OAuthHandler
 
from textblob import TextBlob

import twitter_credentials
import re


handle_list = ["#BTC","#ETH","#USDT","#XRP","#BCH","#ADA","#BSV","#LTC","#LINK","#BNB",
               "#EOS","#TRON","#MKR","#DASH","#YFIDOWN","#XVS","#AAVEUP","#LINKUP",
               "#CTXC","#NPXS","#ZEC","#ZRX","#COCOS","#BAL","#BUSD","#EOS","#TRX","#BNB",
               "#DOT","#YFI","#USDC","#IOST","#MKR","#VET","#NEO","#SXP","#SUSHI","#GRT",
               "#OMG","#EUR","#XMR","#ATOM","#UNI","#XTZ","#ZRX","#THETA","#FIL","#ETHUP",
               "#ONT","#ZIL","#DOGE","#XRPUP","#XRPDOWN","#SXPUP","#RSR","#SNX","#QTUM",
               "#BAND","#SOL","#1INCH","#ALGO","#REN","#SXPDOWN","#CRV","#EGLD","#SRM",
               "#IOTA","#YFII","#NANO","#BUSD","#NEAR","#PAX","#WAVES","#NPXS","#BTCUP",
               "#BAT","#GBP","#AVAX","#CTXC","#LRC","#EOSUP","#KNC","#ALPHA","#MATIC",
               "#KAVA","#TUSD","#COMP","#ICX","#XEM","#ENJ","#STORJ","#LTCUP","#YFIUP",
               "#XRP","#BTCDOWN","#CVC","#OCEAN","#KSM","#HBAR","#LUNA","#BTT","#DNT",
               "#ETHDOWN","#EOSDOWN","#AVAX","#RUNE","#YFIDOWN","#TRX","#HOT","#SKL",
               "#HARD","#LINKUP","#CHZ","#TOMO","#ADAUP","#TRB","#MANA","#XLMUP","#RLC",
               "#ONE","#LINK","#XVS","#FTM","#CTK","#ROSE","#XLMDOWN","#COTI","#SXP",
               "#ARPA","#FLM","#LSK","#RVN","#DGB","#STX","#XTZUP","#TRXUP","#SC","#BNB",
               "#ZEN","#BZRX","#UNFI","#TFUEL","#XLM","#JST","#OXT","#AUD","#REP","#BEL",
               "#DIA","#DOTUP","#SUSHIUP","#REEF","#FET","#AAVEUP","#AXS","#OGN","#NBS",
               "#ANKR","#INJ","#PAXG","#ADADOWN","#ANT","#TRXDOWN","#BLZ","#DCR","#UNIUP",
               "#CTSI","#LINKDOWN","#KEY","#DOTDOWN","#FTT","#WAN","#RIF","#BNT","#LTO",
               "#CHR","#LTCDOWN","#SUSHIDOWN","#FUN","#SAND","#NMR","#AAVEDOWN","#WING",
               "#AUDIO","#WTC","#UTK","#UMA","#WNXM","#CELR","#DATA","#STRAX","#XZC",
               "#IRIS","#HNT","#BNBUP","#PERL","#DENT","#MTL","#ONG","#FILUP","#AKRO",
               "#BTS","#IOTX","#BEAM","#MITH","#WRX","#WIN","#AION","#MBL","#TROY","#SUN",
               "#CHZ","#NULS","#ORN","#PNT","#VTHO","#MFT","#FIO","#XTZDOWN","#DUSK",
               "#KMD","#TCT","#CELO","#VITE","#HIVE","#DOCK","#STMX","#COCOS","#MDT",
               "#ARDR","#DREP","#GTO","#GXS","#AVA","#COS","#UNIDOWN","#BNBDOWN","#NKN",
               "#PSG","#STPT","#SUSD","#FILDOWN","#ATM","#ASR","#OG","#JUV",    
]

handle_list = list(set(handle_list))

class TwitterStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        if status.user.followers_count > 1000 and not hasattr(status, "retweeted_status") and status.lang=="en":
            # Tweet
            if status.truncated == True:
                tweet = status.extended_tweet['full_text']
            else:
                tweet = status.text
            
            #tweet = self.clean_tweet(tweet)
            sentiment = self.analyze_sentiment(tweet)
            
            details = f'Created At : {status.created_at}\n Tweet      : {tweet}\n Fav Count  : {status.favorite_count}\n Followers  : {status.user.followers_count}\n Location   : {status.user.location}\n Sentiment  : {sentiment}\n\n'
            print(details)
            
            with open("out_tweets.csv", "a", encoding='utf-8') as f:
                f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at, tweet, status.favorite_count, 
                                                 status.user.followers_count, status.user.location, 
                                                 sentiment))
    
    def on_error(self, status_code):
        if status_code == 420:
            #return False in case disconnection
            return False

    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1


if __name__ == '__main__':
    with open("out_tweets.csv", "a", encoding='utf-8') as f:
                f.write("created_at,tweet,fav_count,follower_count,location,sentiment\n")
    
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    stream_listener = TwitterStreamListener()
    stream = tweepy.Stream(auth= api.auth, listener = stream_listener)
    
    stream.filter(track=handle_list)
    