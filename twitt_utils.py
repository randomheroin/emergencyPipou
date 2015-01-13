#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Version 1

import tweepy
import os
import re


def file_to_dict(file_name):
    """opens a file and put tab separated values in a dict"""
    d_keys = {}
    with open(file_name, 'r') as f:
        for i in f.readlines():
            i = i[:len(i) - 1]      #Removing the \n char
            j = i.split('\t')
            d_keys[j[0]] = j[1]
        return d_keys


def file_to_list(file_name):
    """opens a file a put each line in a list"""
    liste = []

    with open(file_name, 'r') as f:
        for i in f.readlines():
            i = i[:len(i) - 1]
            i = unicode(i, "utf-8")
            liste.append(i)
    return liste


def twitter_authentication(keys_file):
    """return a tweepy.api object connected to your account"""
    d_keys = file_to_dict(keys_file)
    auth = tweepy.OAuthHandler(d_keys["consumer_key"], 
        d_keys["consumer_secret"])
    auth.set_access_token(d_keys["access_token"], 
        d_keys["access_secret"])
    api = tweepy.API(auth)
    return api

    
def display_time():
    """format hh:mm"""
    time = localtime()
    return str(time[3]) + ":" + str(time[4])

def logging_dms(dm):
    """Log of dms sent by tweets_embues"""
    f = open("tweets.log", 'a')
    f.write(display_time() + "\t" + dm.sender.screen_name.encode('utf-8') + "\t" + 
        dm.text.encode('utf-8') + "\n")
    f.close()

def current_directory():
    """code factoring"""
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    return cur_dir

