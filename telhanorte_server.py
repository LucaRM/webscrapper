# import cgi
# import xml.etree.ElementTree as ET
import cgitb
# import re
import json
# import requests
# import cookiejar
# import itertools
import urllib.request #get the html from url
import asyncio
# import pathlib
# import ssl
import websockets

from bs4 import BeautifulSoup # 

cgitb.enable

async def scrap_telhanorte(websocket, path): # 
    #this scrap with 'tijolo', return 81 items

    query = await websocket.recv() #recives from client

    target = urllib.request.urlopen('http://busca.telhanorte.com.br/busca?q='+query+'&results_per_page=100').read()
    soup = BeautifulSoup(target, "html.parser")
    for item in soup.select("li.nm-product-item"):
        price = item.find('div','nm-offer').find('a','nm-price').get_text()
        if price is not None: #to make sure is the right price
            store = "TLN"
            link = item.find("div", "nm-product-img-container").find("a", "nm-product-img-link")["href"]
            link = "http:" + link
            title = item.find("div", "nm-product-img-container").find("a", "nm-product-img-link")["title"]
            image = item.find("div", "nm-product-img-container").find("a", "nm-product-img-link").find("img")["src"]
            image = "http:" + image
            price = price.replace('por','').replace("Preço","").replace("m²","").replace('R$','').replace('de','').replace('\n','').replace(' ','')
            brand = ''
            try: #send to client
                await websocket.send(store) 
                await websocket.send(link) 
                await websocket.send(title)
                await websocket.send(image)
                await websocket.send(price)
                await websocket.send(brand)
            except:
                print(f'Not found {query}')
                break
                


start_server = websockets.serve(scrap_telhanorte, "localhost", 8765)

try:
    print('starting telha-norte')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except:
    print('Erro: trying to start telha-norte')