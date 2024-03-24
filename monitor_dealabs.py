from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import json
from time import strftime
import time
import re
import os 


with open ('setup.json', 'r') as f:
    j = json.load(f)
    Range = j['Range']
    Webhook = j['Webhook']
    Master_link = j['Master_link']

def found_product(num):
    r = HTMLSession()
    stock = [['',''], ['','']]
    
    x = 1
    y = -1
    while range(int(num)):
        if int(x) == int(num):
            exit()
        
        pat_h = strftime("%H:%M:%S") 
        time.sleep(1)

        base = r.get(Master_link)
        s = BeautifulSoup(base.text, 'lxml')

        article = s.find_all('article', {'class', 'thread cept-thread-item thread--type-list imgFrame-container--scale thread--deal'})

        for target in article:
            div = target.find('strong', {'class','thread-title'})
            break
 
        for result in div :
                    title = result.get('title')
                    href = result.get('href')
                    #print(f'title : {title}\nlink : {href}\n')
                    break
        
        for i in stock :
            if i[0] == title:
                break
        
        if title in i[0]:
                #print(f'Waiting product {x}/{num}.', end='\r')
                stock.append([title, href])
                x +=1
                instance(num, x, y, pat_h)
                
        else :
            stock.append([title, href])
            url = checker_img(href)
            #price = checker_price(href)
            sender(Webhook, title, href, url, '')  
            y += 1  
            #print(f'New product : {title}\n')
            instance(num, x, y, pat_h)
        
def sender(url, title, link, img, price):

    embed = {
        'title' : 'Monitor dealabs .me',
        "description" : "- monitor dealabs",
        "color": 3801229,
        "fields": [
            {"name": "__Title :__", "value": title, "inline": True},
            #{"name": "__Price :__", "value": price, "inline": True},
            {"name": "__Link :__", "value": link, "inline": True},
            {"name": "", "value":"<@441531224557879307>"}
        ],
        
        "thumbnail" : {
            "url" : img
        }
    }  
    
    payload = {
        "content": "",
        "embeds": [embed]
    }

    response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    if response.status_code == 204:
        print('\033[1;32m')
        #print("\033[1;32mWebhook send success.\n")
        pass
    else:
        print("\033[1;31mWebhook error :", response.status_code)

def checker_img(url):
    r = HTMLSession().get(url)
    base = r.text
    s = BeautifulSoup(base, 'lxml')
    
    span = s.find('section')

    for i in span :
        img = i.find_all('div')
        for a in img :
            im = a.find('picture')   
            try :
                for final in im :
                    r_img = final.get('srcset')[0:]
                    return r_img
            except TypeError:
                break
    
def checker_price(url):
    r = HTMLSession()
    base = r.get(url)
    base.html.render()
    print(base)

    s = BeautifulSoup(base.html.html, 'html.parser')
    print(s)
    
    span = s.find('body')
    

    stock = []
    for i in span :
        img = i.find('div', {'id', 'threadDetailPortal'})
        print(img) 

def control(tr, num_range, found):
    pat = str(f'{tr}/{num_range}')
    found = str(found)

    if len(found) == 1 and len(pat) == 6:
        return ('   |')
    elif len(found) == 1 and len(pat) == 7:
        return ('  |')
    elif len(found) == 1 and len(pat) == 8 :
        return (' |')
    elif len(found) == 1 and len(pat) == 9:
        return ('|')
    elif len(found) == 2 and len(pat) == 6:
        return ('  |')
    elif len(found) == 2 and len(pat) == 7:
        return (' |')
    elif len(found) == 2 and len(pat) == 8:
        return ('|')
    elif len(found) == 2 and len(pat) == 9:
        return ('')
    else :
        pass
            
def instance(num_range, tr, found, time):
    os.system('clear')
    print('\033[1;34m')
    print(f"""
 __________________________________
| Monitor Dealabs..  |  By .me     |
|                                  | 
|        TIME : {time}           | 
|__________________________________|
| Found : [{found}] | Range : [{tr}/{num_range}]
|__________________________________|""")

found_product(Range)

#checker_price('https://www.dealabs.com/bons-plans/pc-fixe-ryzen-7-7700-rx-7900xt-20-go-32-go-ram-ddr5-6000-gigabyte-b650-wifi-ssd-nvme-1-to-alim-bequiet-850w-80-gold-2746153')


