# -*- coding: utf-8 -*-

import tweepy


#Lecture des clés d'accès de l'application
f = open("keys.conf", 'r')
consumer_key = f.readline()
consumer_secret = f.readline()
access_token = f.readline()
access_token_secret = f.readline()
f.close()
   
consumer_key = consumer_key[:len(consumer_key) - 1]
consumer_secret = consumer_secret[:len(consumer_secret) - 1]
access_token = access_token[:len(access_token) - 1]
access_token_secret = access_token_secret[:len(access_token_secret) - 1]   
  
#Authentification
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Stuff going on
api = tweepy.API(auth)
user = api.get_user('twitter')

#Liste des followers
followers = tweepy.Cursor(api.followers).items()

#Follow back
for follower in followers:
	print follower.name
	follower.follow()
	

