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


likepost=False
loginform=False
passwordform=False
spam = False
base = 'base.csv'
counter = 0
counterLook = 0
isspam = False
counterSpam = 0
XInstagramAJAX = csrftoken = ds_user_id = sessionid = ig_did = mid = ig_nrcb = shbid = shbts = rur = XIGWWWClaim = False
XIGAppID = "1217981644879628"
print('IGAppid for your version is: '+XIGAppID)
likable = False
photocode = False

if os.path.isfile('login.txt'):
    logins={}
    with open('login.txt','r') as file:
        lgns = file.read().splitlines()
        for i in lgns:
            slic=i.split(":")
            logins[slic[0]]=slic[1]
            
    loginbase = [(k, v) for k, v in logins.items()]
    loginform=loginbase[0][0]
    passwordform=loginbase[0][1]
    print(logins)
    try:
        if 'True' in loginbase[1][1]:
            likepost=True
    except:
        print('Doing follows!')

###############LOADER FUNC
printtags='''
'''
if not os.path.isdir('album'):
    os.mkdir('album')
    print('Directory album created, put you images here!')
if not os.path.isdir('trash'):
    os.mkdir('trash')

    
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
  

##############################################################################

#Открываем сессию и получаем куки
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
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/"})
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        globals()['XInstagramAJAX'] = re.findall(r"rollout_hash\":\"(.*?)\"",r.text)[0]
        
        
        
        


        r = s.post(login_url,data=payload,headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "X-IG-WWW-Claim":'0',
            "x-csrftoken":csrf
        })
        global XIGWWWClaim
        XIGWWWClaim = r.headers['x-ig-set-www-claim']
        print(XIGWWWClaim)
        time.sleep(30)
        
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
            actions()

            
def getcoo():
    headers={
        'Host': 'www.instagram.com',
        'Connection': 'keep-alive',
        ###
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-ASBD-ID': '198387',
        ###
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
        #print(cookies)
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
        #print(cookies)
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
        #print(r.content)
        time.sleep(random.randint(1,5))		
################################################################################        	

def checkuser(username):
    global photocode
    global linkname
    linkname = username
    photocode = False
    media_id=''
    global likable
    likable = False
    link = f'https://www.instagram.com/{username}/?__a=1'
    with requests.Session() as s:

      headers = {

        'Host': 'www.instagram.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-IG-WWW-Claim': XIGWWWClaim,
        'X-Requested-With': 'XMLHttpRequest',
        'X-ASBD-ID': '198387',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-IG-App-ID': XIGAppID,
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://www.instagram.com/{username}/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cookie': f'mid={mid}; ig_did={ig_did}; shbid={shbid}; shbts={shbts}; rur={rur}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
          }  

      r = s.get(link, headers = headers)
      
      try:
        data = json.loads(r.text)
        cookies=dict(r.cookies)
        res = [(k, v) for k, v in cookies.items()]
        for i in res:globals()[i[0]] = i[1]
      except:
          print('bad_data')
          raise
    #########

    try:
        spamcheck = data['spam']
        if spamcheck:
            print('CHECK USER SPAM DETECTED')
            timesleep =  datetime.now() + timedelta(seconds=5000)
            print("SLEEPING from "+str(datetime.now())+" to "+str(timesleep)) 
            time.sleep(10000)
            sessionData()
            time.sleep(600)

    except: print('----------------------------------')                
    try:
        private = data['graphql']['user']['is_private']
        posts = data['graphql']['user']['edge_owner_to_timeline_media']['count']
        followed = data['graphql']['user']['followed_by_viewer']
        follows = data['graphql']['user']['follows_viewer']
        likable = True
        
        if not likepost:           
            if followed or follows:
            #if private or posts < 4 or followed or follows:
                likable = False
                global counterLook
                global counter
                counterLook+=1
                time.sleep(random.randint(20,40))
                if counterLook % 5 == 0:
                    print('Sleeping 5 min to checking')
                    time.sleep(500)
                    #REPLACE COUTER SLEEP TO SENDLIKE FUNCTION AFTER COUNTER ITERATOR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        
                print('@> '+username+' >>>is not valid account!...... LOOKING   '+str(counterLook))

        if likepost:            
            if private or posts < 4 or followed or follows:
                likable = False
                #global counterLook
                #global counter
                counterLook+=1
                time.sleep(random.randint(30,60))
                if counterLook % 5 == 0:
                    print('Sleeping 5 min to checking')
                    time.sleep(300)
                    #REPLACE COUTER SLEEP TO SENDLIKE FUNCTION AFTER COUNTER ITERATOR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        
                print('@> '+username+' >>>is not valid account!...... LOOKING   '+str(counterLook))

    except: print(username+'  page not found')
    if likable:
        photonum=random.randint(0,3)
        photocode=data['graphql']['user']['edge_owner_to_timeline_media']['edges'][photonum]['node']['shortcode']
        if likepost:
            media_id=data['graphql']['user']['edge_owner_to_timeline_media']['edges'][photonum]['node']['id']
            print(username+ f"  >>> Sending like to post > https://www.instagram.com/p/{photocode}/")
        if not likepost:
            media_id=data['graphql']['user']['id']
            print(username+ f"  >>> FOLLOWING")
        
        return media_id

#################################################################################            
def sendlike(media_id):
    global likable
    global isspam
    global counter
    global counterSpam
    ######################### LOGIC TO IF LIKABE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if likable:
        if likepost:        
            linklike = f'https://www.instagram.com/web/likes/{media_id}/like/'
        if not likepost:
            linklike = f'https://www.instagram.com/web/friendships/{media_id}/follow/'
            
        try:
            with requests.Session() as s:

                headers={

                    'Host': 'www.instagram.com',
                    'Connection': 'keep-alive',
                    'Content-Length': '0',
                    'X-IG-WWW-Claim': XIGWWWClaim,
                    'X-Instagram-AJAX': XInstagramAJAX,
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': '*/*',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-ASBD-ID': '198387',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                    'X-CSRFToken': csrftoken,
                    'X-IG-App-ID': XIGAppID,
                    'Origin': 'https://www.instagram.com',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': f'https://www.instagram.com/p/{linkname}/',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
                    'Cookie': f'mid={mid}; ig_did={ig_did}; shbid={shbid}; shbts={shbts}; rur={rur}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
            
                    }
                
                r = s.post(linklike,headers=headers)
                
            liked = json.loads(r.text)
            try:
                spamlike = liked['spam']
                if spamlike:
                    
                    if isspam and counterSpam<10:
                        print('SAVING FROM SPAM! SLEEPING 48 hours.')
                        twodays=random.randint(180000, 200000)
                        timesleep =  datetime.now() + timedelta(seconds=twodays)
                        print("SLEEPING from "+str(datetime.now())+" to "+str(timesleep))
                        isspam=False
                        counterSpam=0
                        time.sleep(int(twodays))
                        sessionData()
                        time.sleep(random.randint(300,600))
                        print('Posting content!')
                        runpost()
                        time.sleep(random.randint(300,600))
                    else:
                        isspam=True
                        print('SPAM DETECTED!')
                        timesleep =  datetime.now() + timedelta(seconds=7200)
                        print("SLEEPING from "+str(datetime.now())+" to "+str(timesleep))
                        time.sleep(7200)
                        sessionData()
                        time.sleep(300)
                    
                    

            except:
                    cookies=dict(r.cookies)
                    res = [(k, v) for k, v in cookies.items()]
                    for i in res:globals()[i[0]] = i[1]

                    counter+=1
                    if isspam:
                        counterSpam+=1
                        print('Counter after spam is '+str(counterSpam))
                        

                        
                    if not likepost:
                        print("  >>> FOLLOWED!....  "+str(counter))
                        print('Sleeping after follow 10-12 min')
                    if likepost:
                        print("  >>> LIKED!....  "+str(counter))
                        print('Sleeping after like 10-12 min')
                    time.sleep(random.randint(530,650))
                    
                    
                    if counter % 3 == 0:
                        print('Sleeping 10 min+')
                        time.sleep(600)
			

                
                    if counter % 50 == 0:
                        print('DOING 50 actions!')
                        doingtime=random.randint(2500,4000)
                        timesleep =  datetime.now() + timedelta(seconds=doingtime)
                        print("SLEEPING from "+str(datetime.now())+" to "+str(timesleep))
                        time.sleep(doingtime)
                        print('POSTING PHOTO!')
                        time.sleep(30)
                        runpost()
                        
            

        except Exception as ee:
            print(ee)
            time.sleep(20)
#######################################################LOADER DATA!
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
        'caption': '',
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
            print('Doing activity')
            time.sleep(random.randint(300,600))
            actions()
            
            
        except Exception as ex:
            print('ERROR!!! ERROR!!! ERROR!!! ERROR!!! ERROR!!!')
            print(ex)
            raise Exception('PhotoLoad ERROR')

            
        destination_path = "Trash"
        new_location = shutil.move(file, destination_path)
        
    else:
        print ("Album is full!")
        raise Exception('Album is full!')
###########################################################

if __name__ == '__main__':
	if not loginform:
		raise ValueError('LOGIN REQUIRED. PLEASE FIL THE LOGINS FILE!!!')	

	sessionData()
	time.sleep(30)
	print("LOGGED IN!")

	with open(f'{base}') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			try:
				if not spam:
					sendlike(checkuser(row[0]))
					with open(f'{base}-log.txt', 'a') as logerfile:logerfile.write(row[0]+'\n')
					
				else:break
			except Exception as err:
				exceptn = str(err)
				print(exceptn)
				print('---------------------------------------')
				continue
