import io
import os
import praw as p
import requests 
from tqdm import tqdm
import textloader as tl
import random
import time
import json

current_dir = os.path.dirname(__file__)

img_links = list()

def PolonaReq():
    URL='https://polona.pl/api/entities/'
    PARAMS={'query':'slowacki', 'size':'1', 'public':'1'}

    r = requests.get(URL, PARAMS)
    data = r.json()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#Uses a POST request to demotmaker.com.pl to generate a demot 
def GenerateDemot():

    demot = tl.GetRandomText()
    imglink = GetRandomLink()
    
    URL='http://www.demotmaker.com.pl/zaawansowane.php'
    PARAMS={'action':'lang=pl','obrazek':'2','tekst':demot[0],'kolor1':'Biały',
    'kolor2':'Biały','rozmiar1':'36','rozmiar2':'16','opis':demot[1],'plik':'','link': imglink,
    'obrobka':'brak','obrot':'brak','kolorobr':'Czarne','rozmiarobr':'2','kolortla':'Czarne'}
    r = requests.post(url = URL, data=PARAMS, files = PARAMS)

    #Finds a direct URL to an generated image
    start = r.text.find("obrazki/")
    end = r.text.find("\"",start)

    url_part=r.text[start:end]

    #Saving to a file
    img_response = requests.get("http://demotmaker.com.pl/"+url_part, stream=True)
    id = 0
    while(os.path.isfile(current_dir+"\\dls\\demot"+str(id)+".jpg")):
        id=id+1
    with open(current_dir+"\\dls\\demot"+str(id)+".jpg", "wb") as handle:
        for data in tqdm(img_response.iter_content()):
            handle.write(data)
        
        print("Created demot: "+str(id)+" with img: "+imglink+" as "+str(demot)) 

    time.sleep(1.5)
    
#Saves streamed data to file
def SaveToFile(filename, content):
    with open(current_dir+"\\dls\\"+filename+".jpg", "wb") as handle:
        for data in tqdm(content.iter_content()):
            handle.write(data)

#Appends links to images from reddit r/hmmm
def RedditTitles(toplimit):
    reddit = p.Reddit(client_id='yd5bYoeRUp7Gfg',client_secret='WWLeGwXepDBVvFYucp6Y4x6hMO8',user_agent='myagent')
    #print(reddit.read_only)
    
    for submission in reddit.subreddit('hmmm').top(limit=toplimit):
        url = submission.url
        if("imgur" in submission.url):
            continue
        
        img_links.append(submission.url)
        #response = requests.get(url, stream=True)
        #SaveToFile(str(submission),response)

def GetRandomLink():
    r = img_links[random.randint(0,len(img_links)-1)]
    return r


print("How many demots you want to generate?")
howmany = int(input())
#Generates demots
print("All demots will be saved in "+current_dir+"/dls/")
RedditTitles(min(howmany*50,4000))
for i in range(1, howmany):
    GenerateDemot()
print("Operation completed!")
<<<<<<< HEAD:src/polonareq.py
PolonaReq()

=======
>>>>>>> parent of 29cb2d0... Update pyquests.py:src/pyquests.py

