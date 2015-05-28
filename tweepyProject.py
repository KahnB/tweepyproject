#This is a Python program that will work in the command line/IDLE and performs basic functions using the Twitter API wrapper Tweepy.
#This must be run in Python 2.7 as the Tweepy version used was compatible with 2.7. This will be updated if Tweepy adds support for Python 3.
#for a sample key, please see the readme.

import tweepy, time, sys, json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import string
from pprint import pprint

def main():
#Had to use keys because basic auth has been deprecated.
#this asks for the consumer and API keys, secrets, and tokens.
    print 'Please login to Twitter to use the app!'
    ckey = raw_input("Enter your consumer key: ")
    if len(ckey) == 25 or 1:
        print 'Key Accepted'
        eCsecret(ckey)
    else:
        print 'Incorrect number of characters.'
        eCkey()
def eCsecret(ckey):
    csecret = raw_input("Enter your consumer secret: ")
    if len(csecret) == 50 or 1:
        print 'Consumer Secret Accepted.'
        eAtoken(ckey,csecret)
    else:
        print 'Incorrect number of characters.'
        eCsecret()
def eAtoken(ckey,csecret):
    atoken = raw_input("Enter your Auth Token ")
    if len(atoken) == 50 or 1:
        print 'Token Accepted.'
        eAsecret(ckey,csecret,atoken)
    else:
        print 'Incorrect number of characters.'
        eAtoken()

def eAsecret(ckey,csecret,atoken):
        asecret = raw_input("Enter your Auth Secret ")
        if len(asecret) == 45 or 1:
            print 'Auth Secret Accepted'
            main2(ckey,csecret,atoken,asecret)
        else:
            print 'Incorrect number of characters.'
            eAsecret()

def main2(ckey,csecret,atoken,asecret):
    print "you typed"
    print ckey
    print csecret
    print atoken
    print asecret
    
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)
    auth = OAuthHandler(ckey, csecret)
    mainMenu(ckey,csecret,atoken,asecret,auth,api)
#this is our main menu function, all other functions call back to this one after executing.	
def mainMenu(ckey,csecret,atoken,asecret,auth,api):
        print("Welcome to the PyTwit app!")
        option=int(input("Please select 1 for home timeline, 2 for tweet, 3 for search, 4 for friends list. "))
        if option==1:
            homeTimeline(ckey,csecret,atoken,asecret,auth,api)
        elif option ==2:
            postTweet(ckey,csecret,atoken,asecret,auth,api)
        elif option ==3:
            searchUsers(ckey,csecret,atoken,asecret,auth,api)
        elif option ==4:
            friendsList(ckey,csecret,atoken,asecret,auth,api)
        else:
            print("Invalid entry, please try again.")
            mainMenu(ckey,csecret,atoken,asecret,auth,api)
#this api call is the closest reproduction to the homepage at twitter.com. It returns the 20 most recent tweets.
#we had significant ASCII errors thanks to emojis and even ellipses, hence the encode.('utf-8') call.
def homeTimeline(ckey,csecret,atoken,asecret,auth,api):
    timeline=api.home_timeline()
    for tweet in timeline:
        user=tweet.user
        name=tweet.user.name
        text=tweet.text
        print(name +"\n"+ text).encode('utf-8')
        print("\n")
    mainMenu(ckey,csecret,atoken,asecret,auth,api)
#this was the simplest function to write, the api call for posting was probably the easiest, and the first one we figured out.
def postTweet(ckey,csecret,atoken,asecret,auth,api):
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    status=raw_input("Write your tweet here: ")
    api.update_status(status)
    print("\n")
    print("Tweet posted!")
    print("\n")
    mainMenu(ckey,csecret,atoken,asecret,auth,api)
	#this function searches for users. The query is limited to ten results on a single page for brevity's sake.
def searchUsers(ckey,csecret,atoken,asecret,auth,api):
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    query=raw_input("Type part or all of the name of the user you are searching for: ")
    users=api.search_users(query,[10],[1])
    for x in users:
        name=x.name
        print(name+ "\n")
    mainMenu(ckey,csecret,atoken,asecret,auth,api)
#this friends list function converts the friend ID key returned by the friends_ids api call into a username through the get_user API call. 
#It also uses API calls to follow and unfollow users.
def friendsList(ckey,csecret,atoken,asecret,auth,api):
    friends=api.friends_ids()
    #pprint(friends)
    for friend in friends:
        friendName=api.get_user(friend)
        print friendName.screen_name
        print ("\n")
    followOrNo=int(input("Would you like to follow or unfollow a user? Press 1 to follow or 2 to unfollow, any other key to return to the main menu."))
    if followOrNo==1:
        friend=raw_input("Please type the name of the user you'd like to follow: ")
        api.create_friendship(friend)
        mainMenu(ckey,csecret,atoken,asecret,auth,api)
    elif followOrNo==2:
        enemy=raw_input("Please type the name of the user you'd like to unfollow: ")
        api.destroy_friendship(enemy)
        mainMenu(ckey,csecret,atoken,asecret,auth,api)
    else:
        print("Please try again.")
        friendsList(ckey,csecret,atoken,asecret,auth,api)
            

main()

