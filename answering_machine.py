#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

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

def repondre(mentions, api, tweets_content, last_mention_id=None):
    try:
        last_mention_id = mentions[0]
    except IndexError:
        pass
    
    if(last_mention_id):
        mentions = api.mentions_timeline(last_mention_id)
    else:
        mentions = api.mentions_timeline()

    for tweet in mentions:
        if is_stand_alone(tweet):
            handle = "@" + tweet.user.screen_name
            word = randomized_word(tweets_content)
            message = handle + " " + word

            api.update_status(message, tweet.id)

    return last_mention_id


if __name__ == "__main__":
    pass