#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import os
from random import randrange
from random import choice
from time import localtime
from time import sleep
from math import ceil

def daemonize():
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.argsstrerror, e.argserrno)
    if (pid == 0):      # Ayanami Rei
        os.setsid()
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, "%s [%d]" % (e.argsstrerror, e.argserrno)
        if (pid == 0):      # Langley Soryu Asuka
            os.chdir("/")
            os.umask(0)
        else:
            os._exit(0)
    else:
        os._exit(0)
    os.open("/dev/null",os.O_RDWR)
    os.dup2(0,1)
    os.dup2(0,2)
    return(0)


def file_to_dict(file_name):
    """opens a file and put tab separated values in a dict"""
    f = open(file_name, 'r')
    d_keys = {}
    for i in f.readlines():
        i = i[:len(i) - 1]        #Removing the \n char
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
		try:
			num = int(j[0])
			word = unicode(str(j[1]), 'utf-8')
			for j in range(int(num)):
				d_words[n] = word
				n += 1
		except ValueError:
			pass
			
	return d_words
	

def randomized_word(d_words):
    """Selects a random word from a probability dict"""
    p = randrange(len(d_words))
    return d_words[p]

def twitter_authentification(keys_file):
    """return a tweepy.api object connected to your account"""
    d_keys = file_to_dict(keys_file)
    auth = tweepy.OAuthHandler(d_keys["consumer_key"], 
        d_keys["consumer_secret"])
    auth.set_access_token(d_keys["access_token"], 
        d_keys["access_secret"])
    api = tweepy.API(auth)
    return api

def fonctionnement_principal():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    api = twitter_authentification(cur_dir + "/keys.conf")

    seconds_by_day = 86400
    tweets_content = file_to_probability_dict(cur_dir + "/words.conf")
    monday = 0
    
    followers = set(api.followers())
    nb_followers = len(followers)
    messaged_followers = set()
    followers_by_day = ceil(nb_followers / 7.0)

    last_mention_id = None
    mentions = []
    while 1:
        if localtime()[6] == monday:    #Actualize followers list (on monday)
            try:
                followers = set((api.followers))
            except tweepy.error.TweepError:
                pass
            nb_followers = len(followers)
            messaged_followers = set()
            followers_by_day = ceil(nb_followers / 7.0)
        
        today = localtime()[6]
        tweets_content = file_to_probability_dict(cur_dir + "/words.conf")
    
        while localtime()[6] == today:
            time_gap = seconds_by_day / followers_by_day        
            to_be_messaged = list(followers - messaged_followers)

            #Pick a user to message
            selected_user = choice(to_be_messaged)
            messaged_followers.add(selected_user)
    
            #Putting together the "message"
            handle = "@" + selected_user.screen_name
            word = randomized_word(tweets_content)
            message = handle + " " + word
            try:
                api.update_status(message)
            except tweepy.error.TweepError:
                pass
            
            last_mention_id = repondre(mentions, api, last_mention_id, tweets_content)
            sleep(time_gap)


def is_stand_alone(tweet):
    if(tweet.in_reply_to_status_id):
        return False
    return True


def repondre(mentions, api, tweets_content, last_mention_id=None):
    try:
        last_mention_id = mentions[0]
    except IndexError:
        pass

    mentions = api.mentions_timeline(last_mention_id)

    for tweet in mentions:
        if is_stand_alone(tweet):
            handle = "@" + tweet.user.screen_name
            word = randomized_word(tweets_content)
            message = handle + " " + word

            api.update_status(message, tweet.id)

    return last_mention_id


if __name__ == "__main__":

    fonctionnement_principal()
