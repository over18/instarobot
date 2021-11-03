import json
import subprocess
import random
import time
import csv
import re
import requests
from datetime import datetime, timedelta
import os
from PIL import Image
import glob
import shutil
from os import path

print('''Hello. I am a instagram bot, who uploading random photo across your accounts list round robin.
Now if I don't find, im create two folders. Plz put the photos in "album" folder.
In folder "trash" will be processed photos after posting.
Fill the question. Enter login and password.
Also you must set time range to define frequency of your posting. From and to in seconds (in default it is 20000 to 30000 equivalent ~7 to 10 hours).

Note! Fill up the directory "album" before starting.

---You can use telegram bot "tgbot.py" to top up album.---
__________________________________________________________________________
''')

if not os.path.isdir('album'):
    os.mkdir('album')
    print('Directory album created, put you images here!')
if not os.path.isdir('trash'):
    os.mkdir('trash')    

loginform=input('Login:  ') or ""
passwordform=input('Password:  ') or ""
#########################################
####Here your logins and passwords.#####
########################################

frfrom=input('Frequency from (seconds):  ') or "80000"
frto=input('Frequency to (seconds):  ') or "86000"
frfrom=int(frfrom)
frto=int(frto)

spam = False
XInstagramAJAX = csrftoken = ds_user_id = sessionid = ig_did = mid = ig_nrcb = shbid = shbts = rur = XIGWWWClaim = False
XIGAppID = input('Paste XIGAppID or press enter to default: ') or "1217981644879628"
print('IGAppid for your version is: '+XIGAppID)


printtags='''
'''

def taggen():
    with open('tags.txt','r') as file:
        tags = file.read().splitlines()

        random.shuffle(tags)
        cnttag=random.randint(10,15)
        text = ' '.join(tags[:cnttag])

        capt=f'''.
.
.
{text}'''
        return capt

def smilegen():
    with open('smiles.txt','r', encoding='utf-8') as file:
        smiles = file.read().splitlines()
        texts=['See my bio','Look at bio','Link in bio', 'Visit my bio', 'More in bio', 'Click my bio', 'Visit my page', 'Find me in bio', 'Looking for fun', 'Let\'s get to know better.', 'Have a nice day!']
        random.shuffle(smiles)
        rantext=texts[random.randint(0,(len(texts)-1))]
        smiletext = ''.join(smiles)
        captiontext=f'{rantext} {smiletext}'
        return captiontext


def locgen():
    locations={}
    with open('locations.txt','r') as file:
        locs = file.read().splitlines()
        
        for i in locs:
            slic=i.split(":")
            locations[slic[0]]=slic[1]
            
            
    locbase = [(k, v) for k, v in locations.items()]

    loc=locbase[random.randint(0,len(locbase))]
    print('Use location: '+loc[0])
    return loc[1]    
    
def jpeg_res(filename):
   """"This function prints the resolution of the jpeg image file passed into it"""

   # open image for reading in binary mode
   with open(filename,'rb') as img_file:

       # height of image (in 2 bytes) is at 164th position
       img_file.seek(163)

       # read the 2 bytes
       a = img_file.read(2)

       # calculate height
       height = (a[0] << 8) + a[1]

       # next 2 bytes is width
       a = img_file.read(2)

       # calculate width
       width = (a[0] << 8) + a[1]
    
   print("The resolution of the image is",width,"x",height)
   return width, height    
 
def tspose(filename):
    im = Image.open(filename)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im.save(filename)
    
#Open session
def sessionData():
    global XIGWWWClaim
    #link = 'https://www.instagram.com/accounts/login/'
    link = 'https://www.instagram.com/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    localtime = int(datetime.now().timestamp())

#Login and password.
    payload = {
        'username': loginform,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{localtime}:{passwordform}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
#Cookie and headers req.
    with requests.Session() as s:
        r = s.get(link, headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/"})
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        globals()['XInstagramAJAX'] = re.findall(r"rollout_hash\":\"(.*?)\"",r.text)[0]
        coo = dict(r.cookies)
        
        
        


        r = s.post(login_url,data=payload,headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "X-IG-WWW-Claim":'0',
            "x-csrftoken":csrf
        })
        global XIGWWWClaim
        XIGWWWClaim = r.headers['x-ig-set-www-claim']
        
        if r.status_code==403 or r.status_code==429:
            global spam 
            spam = True
            print("ERROR "+str(r.status_code)+" >>> "+r.text)
            timesleep =  datetime.now() + timedelta(seconds=10000)
            print("SLEEPING from "+str(datetime.now())+" to "+str(timesleep))
            time.sleep(10000)
            sessionData()
            

        else:
            cookies=dict(r.cookies)
            res = [(k, v) for k, v in cookies.items()]
            for i in res:globals()[i[0]] = i[1]
            print(r.status_code)
            print('\n\nConnected.')
            
            getcoo()
            time.sleep(random.randint(0,3))
            actions()
            

def getcoo():
    headers={
        'Host': 'www.instagram.com',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'X-ASBD-ID': '198387',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-User': '?1',
        'Referer': 'https://www.instagram.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cookie': f'ig_did={ig_did}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
            }

   

    with requests.Session() as s:
        r = s.get('https://www.instagram.com/accounts/onetap/?next=%2F', headers=headers)
        print('Cookies catched.')
        print(r.status_code)
        #print('GET COOK')
        cookies=dict(r.cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]
                
def actions():

###REELSTRAY

    headers={
        'Host': 'i.instagram.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-IG-WWW-Claim':XIGWWWClaim,
        'X-ASBD-ID': '198387',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'X-IG-App-ID': XIGAppID,
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cookie': f'mid={mid}; ig_did={ig_did}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}; rur={rur}',
            }

   

    with requests.Session() as s:
        
        r = s.get('https://i.instagram.com/api/v1/feed/reels_tray/', headers=headers)
        print('Cookies catched.')
        print('Reels_tray code: '+str(r.status_code))
        
        cookies=dict(r.cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]

        time.sleep(random.randint(1,5))


       

    ####TIMELINE

        headers={
            'Host': 'i.instagram.com',
            'Connection': 'keep-alive',
            'Content-Length': '153',
            'X-IG-WWW-Claim': XIGWWWClaim,
            'X-Instagram-AJAX': XInstagramAJAX,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'X-ASBD-ID': '198387',
            'X-CSRFToken': csrftoken,
            'X-IG-App-ID': XIGAppID,
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.instagram.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Cookie': f'mid={mid}; ig_did={ig_did}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}; rur={rur}',
                }

        body={

            'device_id': ig_did,
            'is_async_ads_rti': '0',
            'is_async_ads_double_request': '0',
            'rti_delivery_backend': '0',
            'is_async_ads_in_headload_enabled': '0',

        }

        r = s.post('https://i.instagram.com/api/v1/feed/timeline/', data=body, headers=headers)
        print('timeline catched.')
        cookies=dict(r.cookies)
        print(cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]


        print('timeline code: '+str(r.status_code))
        time.sleep(random.randint(1,5))


    ###########BADGE


        headers={
            'Host': 'i.instagram.com',
            'Connection': 'keep-alive',
            'Content-Length': '67',
            'X-IG-WWW-Claim': XIGWWWClaim,
            'X-Instagram-AJAX': XInstagramAJAX,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'X-ASBD-ID': '198387',
            'X-CSRFToken': csrftoken,
            'X-IG-App-ID': XIGAppID,
            'Origin': 'https://www.instagram.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.instagram.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Cookie': f'mid={mid}; ig_did={ig_did}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}; rur={rur}',
                }

        body={
            'user_ids': ds_user_id,
            'device_id': ig_did,

        }

        r = s.post('https://i.instagram.com/api/v1/notifications/badge/', data=body, headers=headers)
        cookies=dict(r.cookies)
        print(cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]


        print('badge catched.')
        print('badge code: '+str(r.status_code))
        time.sleep(random.randint(1,5))

    ########MAINFEST

        headers={
                'Host': 'www.instagram.com',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                'Accept': '*/*',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'manifest',
                'Referer': f'https://www.instagram.com/{loginform}/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
                
                    }



        r = s.get('https://www.instagram.com/data/manifest.json', headers=headers)

        print('MAINFEST catched.')
        print('MAINFEST code: '+str(r.status_code))
        print(r.content)
        time.sleep(random.randint(1,5))


                
def photoload(imagefile):
    with requests.Session() as s:
        filelengh = os.path.getsize(imagefile)
        lengh=str(filelengh)

        im = Image.open(imagefile)
        (imwidth, imheight) = im.size
        #(imwidth, imheight) = jpeg_res(imagefile)


        mtime = int(datetime.now().timestamp())
        microtime = str(mtime)
        #print(microtime)
        #print('width is: ' + str(imwidth) + '......height is: ' + str(imheight))
        headers={
                            'Host': 'i.instagram.com',
                            'Connection': 'keep-alive',
                            'Content-Length': lengh,
                            'X-Entity-Type': 'image/jpeg',
                            'X-IG-App-ID': XIGAppID,
                            'X-Entity-Name': f'fb_uploader_{microtime}',
                            'Offset': '0',                            
                            'X-Instagram-AJAX': XInstagramAJAX,
                            'Content-Type': 'image/jpeg',
                            'Accept': '*/*',
                            'X-Instagram-Rupload-Params': f'{{"media_type":1,"upload_id":{microtime},"upload_media_height":{imheight},"upload_media_width":{imwidth}}}',
                            'X-ASBD-ID': '198387',
                            'X-Entity-Length': lengh,
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
                            'Origin': 'https://www.instagram.com',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.instagram.com/',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
                            "Cookie": f'mid={mid}; ig_did={ig_did}; shbid={shbid}; shbts={shbts}; rur={rur}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
                        }

        r = s.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{microtime}', data=open(imagefile, "rb"), headers=headers)
        print('\n\n'+str(r.status_code))
        print(r.text)
        print('\nWaiting a few seconds...')
        cookies=dict(r.cookies)
        print(cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]

        time.sleep(random.randint(5,25))
        
        
        sheaders={
        'Host': 'i.instagram.com',
        'Connection': 'keep-alive',
        'Content-Length': '525',
        'X-IG-App-ID': XIGAppID,
        'X-IG-WWW-Claim': XIGWWWClaim,
        'X-Instagram-AJAX': XInstagramAJAX,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'X-ASBD-ID': '198387',
        'X-CSRFToken': csrftoken,
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cookie': f'mid={mid}; ig_did={ig_did}; fbm_124024574287414=base_domain=.instagram.com; shbid={shbid}; shbts={shbts}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}; rur={rur}',
            }


        printtags=taggen()
        comm = smilegen()
        
        sbody = {


        'source_type': 'library',
        #'caption': f'{comm}\n{printtags}',
        'caption': f'{comm}',
        'upcoming_event':'' ,
        'upload_id': microtime,
        'geotag_enabled': 'true',
        'location': f'{{"facebook_places_id":{locgen()}}}',
        'usertags':'' ,
        'custom_accessibility_caption':'', 
        'disable_comments': '0',

            
            }

        r = s.post('https://www.instagram.com/create/configure/', data=sbody, headers=sheaders)

        print('\n\n'+str(r.status_code))
        print(sbody)
        cookies=dict(r.cookies)
        print(cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]
        


        
def runpost():
    
    sessionData()
    print('Logged in >>> '+loginform+' <<< Waiting 5-10min to post.')
    time.sleep(random.randint(300,600))
    while True:
        
            
        time.sleep(1)
        mkfiles = glob.glob("album/*.jpg")#Collecting photos.
        try:
            numb=random.randint(0,(len(mkfiles)-1))
            
        
        except: print(bool(mkfiles))
        if bool(mkfiles):
            file = mkfiles[int(numb)]
            tspose(file)
            try:
                photoload(file)               
                print('Post from '+loginform+' with '+file+' created.')
                print('Doing activity 30-60min')
                time.sleep(random.randint(1800,3700))
                actions()
                
                
            except Exception as ex:
                print('ERROR!!! ERROR!!! ERROR!!! ERROR!!! ERROR!!!')
                print(ex)
                break
                
            destination_path = "Trash"
            new_location = shutil.move(file, destination_path)
            
            global frfrom
            global frto
            sltime=random.randint(frfrom,frto)
            tsleep =  datetime.now() + timedelta(seconds=sltime)
            print("SLEEPING from "+str(datetime.now())+" to "+str(tsleep))
            time.sleep(sltime)
        else:
            print ("Album is full!")
            break

if __name__ == "__main__":
    runpost()
