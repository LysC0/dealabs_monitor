"""
Dealabs Monitor
@LysC0
"""

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import json
from time import strftime
import time
import os 

with open ('setup.json', 'r') as f:
    stock_main = []
    j = json.load(f)
    Range = j['Range']
    Webhook = j['Webhook']
    Master_link = j['Master_link']
    keyword = j['Keyword']

    for i in keyword :
        stock_main.append(i)

def found_product(num):
    r = HTMLSession()
    stock = [['',''], ['','']]
    
    x = 1
    y = -1
    while range(int(num)):
        if int(x) == int(num):
            exit()
        
        pat_h = strftime("%H:%M:%S") 
        time.sleep(0.4)

        base = r.get(Master_link)
        s = BeautifulSoup(base.text, 'lxml')

        article = s.find_all('article', {'class', 'thread cept-thread-item thread--type-list imgFrame-container--scale thread--deal'})

        for target in article:
            div = target.find('strong', {'class','thread-title'})
            break
 
        for result in div :
                    title = result.get('title')
                    href = result.get('href')
                    break
        
        for i in stock :
            if i[0] == title:
                break
        
        if title in i[0]:
                stock.append([title, href])
                x +=1
                instance(num, x, y, pat_h)
                
        else :
            stock.append([title, href])
            url = checker_img(href)
            sender(Webhook, title, href, url, '')  
            y += 1
            instance(num, x, y, pat_h)
        
def sender(url, title, link, img, price):
    stock = []
    stock.append(title)
    
    for i in stock_main : 
        if i.lower() in title.lower() :
            title = stock[0]
            embed = {
                'title' : f'Monitor dealabs .me /:white_check_mark: Keyword **__{i}__** Found :white_check_mark:',
                "description" : "- monitor dealabs",
                "color": 3120166,
                "fields": [
                    {"name": "__Title :__", "value": title, "inline": True},
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
            else:
                print("\033[1;31mWebhook error :", response.status_code)
    embed = {
        'title' : 'Monitor dealabs .me',
        "description" : "- monitor dealabs",
        "color": 3801229,
        "fields": [
            {"name": "__Title :__", "value": title, "inline": True},
            {"name": "__Link :__", "value": link, "inline": True},
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
    os.system('cls') #windows clear
    #os.system('clear') #mac/linux clear
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

"""
add feature : 
. price in webhook
. proxy 
. undetectable
"""



