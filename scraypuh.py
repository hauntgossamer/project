import praw
import requests
import json
from tqdm import tqdm
import sys
import time
import os, subprocess
import random

secret = os.getenv('SECRET')
sys.tracebacklimit = 0

reddit = praw.Reddit(
    client_id="R8z5r-te9mGxDjJ5-eDnKQ", 
    client_secret=f"{secret}", 
    user_agent="scraypuh")

def getsumn(subreddit, limit=None):
    response = requests.post(api, data={"subreddit": subreddit, "limit":limit})
    return response.content

def sub_exists(subreddit):
    exists = False
    try:
        reddit.subreddits.search_by_name(subreddit,  exact=True)
        exists = True
    except:
        exists = False
    return exists

def scrape():
    picked_subreddit = input("Welcome to Deskly, your desktop companion! Pick a subreddit, and make sure you OMIT the 'r/'! \n")
    picked_time = input("Enter a time in seconds for how long each image should be shown (10 second minimum required, 60 second minimum recommened):\n")
    if int(picked_time) < 10:
        print("Time must be longer than ten minutes! Please start over...")
        return        
    picked_width = input("Pick a width for your window:\n")
    picked_height = input("Pick a height for your window:\n")
    print("Please wait while I scrape your chosen subreddit...\nThis process can take up to 5 minutes, please be patient. You'll have a buffer of 5 images to start with, the rest will come once the process is complete!")

    iurls = []
    write_to_file = []
    count = 0
    noimgcount = 0
    if sub_exists(picked_subreddit):
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

        progress = tqdm(desc=f"Searching for images in the top 100 posts on r/{picked_subreddit}!")
        first6 = tqdm(desc="Buffer", total=5)
        posts = getsumn(picked_subreddit, 5)
        os.system("./fixdir.sh")
        for post in posts:
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
                            first6.update(1)
                        else:
                            first6.update(1)
                            noimgcount = noimgcount + 1
                    else:
                        first6.update(1)
                        noimgcount = noimgcount + 1
                except:
                    first6.update(1)
                    noimgcount = noimgcount + 1
                    continue
        picnum = 1
        for i in iurls[0:5]:
            subprocess.Popen([f"./sendtofeh.sh {i} {picnum}"], shell=True)
            picnum = picnum + 1
            time.sleep(0.3)
        subprocess.Popen([f"./runfeh.sh {picked_width} {picked_height} {picked_time}"], shell=True)
        posts = getsumn(picked_subreddit, 100)
        for post in posts:
                indpost = f"https://reddit.com/r/{picked_subreddit}/comments/{post}/.json"
                page = requests.get(indpost, headers = {'User-agent': 'scraypuh'}).json()
                try:
                    img = page[0]["data"]["children"][0]["data"]["url_overridden_by_dest"]
                    if "img" or "png" or "jpg" or "gallery" in img:    
                        if "v." not in img:
                            iurls.append(img)
                            write_to_file.append(img)
                            write_to_file.append("\n\n")
                            progress.update(1)
                            count = count + 1
                        else:
                            noimgcount = noimgcount + 1
                            progress.update(1)
                            noimgcount = noimgcount + 1
                    else:
                        noimgcount = noimgcount + 1
                        progress.update(1)
                        noimgcount = noimgcount + 1        
                except:
                    progress.update(1)
                    noimgcount = noimgcount + 1
                    continue            

        progress.close()
        print(f"\nFound {count} images! \n")
        print(f"\n\n{noimgcount} posts did not have images.")
    for i in tqdm(iurls, desc="Saving images temporarily!", total=count):
        os.system(f"./sendtofeh.sh {i} {picnum}")
        time.sleep(0.3)
        picnum = picnum + 1
    os.system("./killfeh.sh")
    print("Starting the full slideshow in 5 secs...")
    time.sleep(5)
    os.system(f"./runfeh.sh {picked_width} {picked_height} {picked_time}")

scrape()