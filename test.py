import praw #reddit posting
import sys #system
import urllib #view websites
import time #get time
import os, shutil
from threading import Thread
import functools
import subprocess
import schedule
#C:\Users\C-Laptop\AppData\Local\Programs\Python\Python35-32\Scripts
def unic(msg): #convert text for saving in .txt
    return msg.encode("utf-8")





def timeout(timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout)
            except Exception as je:
                print ('error starting thread')
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco
   

def loadmemebot():
    #REmoves Images:
    folder = 'images'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
   
    print("opening file..") #open output in writing mode
    target = open("output.txt", "w")
 
    print("removing file..") #reset output
    target.truncate()
 
    print("writing file..")
 
    user_agent = ("Mr Snuggles") #information sent to websites when i load them
    minScore = 50 #minimum score a post can have before i steal it
 
    r = praw.Reddit(client_id = "ergGTI1-ZxRylQ",
    client_secret = "XEjnRrK3M784yhijG9gS5VnQAtE",
    user_agent = user_agent) #get on reddit as a visitor opened in user_agent
 
    subreddit = r.subreddit("funny")
 
    submissions = subreddit.top("week", limit = 1000) #get_top_from_all get_hot top_from_week #getting submissions as a table
 
    with open('cache.txt', 'r') as cache: #go through all the cached posts
        existing = cache.read().splitlines()


    #open('cache.txt', 'w').close()   
    with open('cache.txt', 'a+') as cache: #with cache open

        for submission in submissions: #go through all submissions gathered
            print(submission.url) #show the url
            #with open('list.txt', 'a+') as linklist:
            #    linklist.write(submission.url + "\n")
            time.sleep(0.02) #wait so i can watch it work
            #the line below is a mess, it checks if the submission hasn't been grabbed, then if the domain is valid and the score is okay
            if submission.id not in existing and submission.score > minScore and (submission.domain == "i.imgur.com" or submission.domain == "m.imgur.com" or submission.domain == "imgur.com") and ('.gif' not in submission.url or '.jpg' in submission.url or '.png' in submission.url or '.JPEG' in submission.url):
                print("adding "+submission.id+" to cache") #if it's okay, say so
                existing.append(submission.id)
                cache.write(submission.id + "\n")
                with open('list.txt', 'a+') as linklist:
                    linklist.write(submission.url + "\n")                  
                target.write(str(unic(str(submission.title)))+" ("+submission.id+")") #record info from post in output
                target.write("\n")
                target.write(str(submission.score))
                target.write("\n")
                target.write("---------")
                target.write("\n")
            elif submission.id not in existing: #why i had that whole thing in one line
                existing.append(submission.id) #cache this submission
                cache.write(submission.id + "\n")
           
    target.close() #unload the text




def job(t):
    func = timeout(timeout=300)(loadmemebot())
    try:
        func()
    except:
        print("Stop Right there scuM!")
        pass #handle errors here

schedule.every().day.at("19:48").do(job,"19:48")

while True:
    print("WAITING FOR TIMER")
    schedule.run_pending()
    time.sleep(60) # wait one minute