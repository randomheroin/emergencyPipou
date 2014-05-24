# -*- coding: utf-8 -*-

#import tweepy
from random import randrange

def file_to_dict(file_name):
	"""opens a file and put tab separated values in a dict"""
	f = open(file_name, 'r')
	d_keys = {}
	for i in f.readlines():
		i = i[:len(i) - 1]		#Removing the \n char
		j = i.split('\t')
		d_keys[j[0]] = j[1]

	return d_keys

def file_to_probability_dict(file_name):
	"""opens a file and put tab separated values in a probability dict"""
	f = open(file_name, 'r')
	d_words = {}
	n = 0
	for i in f.readlines():
		i = i[:len(i) - 1]		#Removing the \n char
		j = i.split('\t')
		num = int(j[0])
		word = str(j[1])
		for j in range(int(num)):
			d_words[n] = word
			n += 1
			
	return d_words
	

def randomized_words(d_words):
	"""Selects a random word from a probability dict"""
	p = randrange(len(d_words))
	return d_words[p]

print file_to_probability_dict("words.conf")

#Lecture des clés d'accès de l'application
d_keys = file_to_dict("keys.conf")

#Authentification
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Stuff going on
api = tweepy.API(auth)
user = api.get_user('twitter')

#Liste des followers
followers = tweepy.Cursor(api.followers).items()
nb_followers = len(followers)



	

