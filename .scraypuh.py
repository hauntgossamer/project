import praw
import requests
import json
from tqdm import tqdm
import sys
import time
import os, subprocess
import random

api = "https://secretapi.onrender.com"
secret = requests.get(api).json()["secret"]
reddit = praw.Reddit(
    client_id="R8z5r-te9mGxDjJ5-eDnKQ", 
    client_secret=secret, 
    user_agent="scraypuh")
reddit.read_only=True
def getsumn(subreddit, limit=None):
    response = reddit.subreddit(subreddit).top(limit=limit)
    return response

def sub_(subreddit):
    exists = False
    reddit.subreddits.search_by_name(subreddit,  exact=True)
    time.sleep(0.3)
    exist = reddit.subreddits.search_by_name(subreddit,  exact=True)
    exists = True
    if exist == []:
        print("Sorry, that subreddit doesn't exist! Did you type it correctly?")
        exists = False
    else:
        try:
            posts = reddit.subreddit(subreddit).top(limit=1)
            for post in posts:
                indpost = f"https://reddit.com/r/{picked_subreddit}/comments/{post}/.json"
                page = requests.get(indpost, headers = {'User-agent': 'scraypuh'}).json()
        except Exception as e:
            if "403" in e.args[0]:
                print("Sorry, that subreddit can't be accessed without credentials! Try another!")
                exists = False 
            if "404" in e.args[0]:
                print("Sorry, that subreddit doesn't exist! Did you type it correctly?")
                exists = False
    return exists 

def scrape():
    picked_width = None
    picked_height = None
    picked_time = None
    picked_subreddit = input("Welcome to Scraypuh, your desktop subreddit scraping companion! Pick a subreddit, and make sure you OMIT the 'r/'! \n")
    print("Please wait...")
    if sub_(picked_subreddit):
        pass
    else: return
    picked_time = input("Enter a time in seconds for how long each image should be shown (10 second minimum required, 60 second minimum recommened)\n You can also press ENTER if you want to just go with the default time limit of 60 seconds and the default size of 640x480px:\n")

    if type(int(picked_time)) == int:
        if int(picked_time) < 10:
                print("Time must be longer than ten sconds! Please start over...")    
                return
        else:
            picked_width = input("Pick a width for your window:\n")
            picked_height = input("Pick a height for your window:\n")
    else:
        pass  
    
    print("\n\nPlease wait while I scrape your chosen subreddit...\nThis process can take up to 5 minutes, please be patient. \nYou'll have a buffer of 5 images to start with, the rest will come once the process is complete!")

    iurls = []
    count = 0
    noimgcount = 0
    if sub_(picked_subreddit):
        try:
            posts = getsumn(picked_subreddit, 5)
            for post in posts:
                continue
        except Exception as e:
            if "403" in e.args[0]:
                print("Sorry, that subreddit can't be accessed without credentials! Try another!")
                return
            if "value" in e.args[0]:
                print("Sorry, that subreddit doesn't exist! Did you type it correctly?")
                return

        progress = tqdm(desc=f"Searching for images in the top 100 posts on r/{picked_subreddit}!", total=100)
        print("\n")
        print("\n")
        posts = getsumn(picked_subreddit, 5)
        os.system("./.fixdir.sh")
        for post in tqdm(posts, desc="Buffer", total=5):
                indpost = f"https://reddit.com/r/{picked_subreddit}/comments/{post}/.json"
                page = requests.get(indpost, headers = {'User-agent': 'scraypuh'}).json()
                try:
                    img = page[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]
                    if "img" or "png" or "jpg" or "gallery" in img:    
                        if "v." not in img:
                            iurls.append(img)
                            write_to_file.append(img)
                            write_to_file.append("\n\n")
                            count = count + 1
                        else:
                            noimgcount = noimgcount + 1
                    else:
                        noimgcount = noimgcount + 1
                except:
                    noimgcount = noimgcount + 1
                    continue
        picnum = 1
        for i in iurls[0:5]:
            subprocess.Popen([f"./.sendtofeh.sh {i} {picnum}"], shell=True)
            picnum = picnum + 1
            time.sleep(0.3)
        subprocess.Popen([f"./.runfeh.sh {picked_width if picked_width is not None else 640} {picked_height if picked_height is not None else 480} {picked_time if picked_time is not None else 60}"], shell=True)
        
        posts = getsumn(picked_subreddit, 100)
        for post in posts:
                indpost = f"https://reddit.com/r/{picked_subreddit}/comments/{post}/.json"
                page = requests.get(indpost, headers = {'User-agent': 'scraypuh'}).json()
                try:
                    img = page[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]
                    if "img" or "png" or "jpg" or "gallery" in img:    
                        if "v." not in img:
                            iurls.append(img)
                            progress.update(1)
                            # print("found a video :/")
                            count = count + 1
                            # print(count)
                        else:
                            progress.update(1)
                            count = count + 1
                            # print("finally found an image!")
                            # print(count)
                    else:
                        progress.update(1)
                        noimgcount = noimgcount + 1
                        # print(f"No image here: {noimgcount}")       
                        # print(count)
                except:
                    progress.update(1)
                    noimgcount = noimgcount + 1
                    # print("No image here")
                    # print(count)
                    continue            

        progress.close()
        print(f"\nFound {count} images!")
        print(f"{noimgcount} posts did not have images.")
    for i in tqdm(iurls, desc="Saving images temporarily!", total=count):
        os.system(f"./.sendtofeh.sh {i} {picnum}")
        time.sleep(0.3)
        picnum = picnum + 1
    os.system("./.killfeh.sh")
    print("Starting the full slideshow in 5 secs...")
    time.sleep(5)
    subprocess.Popen([f"./.runfeh.sh {picked_width if picked_width is not None else 640} {picked_height if picked_height is not None else 480} {picked_time if picked_time is not None else 60}"], shell=True)
    print("Enjoy your slideshow!")
scrape()
