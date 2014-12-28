#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import os
from twitt_utils import *
from random import randrange
from random import choice
from time import localtime
from time import sleep
from math import ceil


def fonctionnement_principal():
    cur_dir = current_directory()
    api = twitter_authentification(cur_dir + "/keys.conf")

    seconds_a_day = 86400
    tweets_content = file_to_list(cur_dir + "/words.conf")
    MONDAY = 0
    
    followers = set(api.followers())
    nb_followers = len(followers)
    messaged_followers = set()
    followers_by_day = ceil(nb_followers / 7.0)
    
    while 1:
        if localtime()[6] == MONDAY:    #Actualize followers list (on monday)
            try:
                followers = set(api.followers())
            except tweepy.error.TweepError:
                pass
            nb_followers = len(followers)
            messaged_followers = set()
            followers_a_day = ceil(nb_followers / 7.0)
        
        today = localtime()[6]
        tweets_content = file_to_list(cur_dir + "/words.conf")
    
        while localtime()[6] == today:
            time_gap = seconds_a_day / followers_a_day        
            to_be_messaged = list(followers - messaged_followers)

            #Pick a user to message
            selected_user = choice(to_be_messaged)
            messaged_followers.add(selected_user)
    
            #Putting together the "message"
            handle = "@" + selected_user.screen_name
            word = choice(tweets_content)
            message = handle + " " + word
            try:
                api.update_status(message)
            except tweepy.error.TweepError:
                pass
            
            sleep(time_gap)


if __name__ == "__main__":

    fonctionnement_principal()
