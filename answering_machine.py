#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
from os import path.isfile

def is_stand_alone(tweet):
    """Is the tweet a reply"""
    if(tweet.in_reply_to_status_id):
        return False
    return True

def is_reply_to_me(tweet, api):
    """Is the tweet in reply to one of mine"""
    if(tweet.in_reply_to_screen_name == api.me.screen_name):
        return True
    return False

def repondre(mentions, last_mention, api, tweets_content):
    
    mentions = api.mentions_timeline(last_mention)

    for tweet in mentions:
        if is_stand_alone(tweet):
            handle = "@" + tweet.user.screen_name
            word = randomized_word(tweets_content)
            message = handle + " " + word

            api.update_status(message) #reply_to=tweet.id)

    try:
        last_mention = mentions[0].id
        save_last_mention(last_mention)
    except IndexError:
        pass


def save_last_mention(last_mention, filename = "last_mention"):
    with open(filename, 'w') as f:
        f.write(last_mention)

def read_last_mention(filename = "last_mention"):
    with open(filename, 'r') as f:
        return int(f.read())

def main():

    SLEEP_TIME = 300        # 5 minutes

    cur_dir = current_directory()
    api = twitter_authentication(cur_dir + "/keys.conf")
    tweets_content = file_to_list(cur_dir + "/words.conf")
    last_mention = int()

    if(isfile("last_mention")):
        last_mention = read_last_mention()
        mentions = []
    else:
        mentions = api.mentions_timeline()
        last_mention = mentions[0].id
        save_last_mention(last_mention)

    while 1:
        last_mention = read_last_mention()
        repondre(mentions, last_mention, api, tweets_content)
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()