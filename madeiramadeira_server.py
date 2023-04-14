import cgitb
import json
import urllib.request #get the html from url
import asyncio
import websockets

from bs4 import BeautifulSoup 

cgitb.enable

async def scrap_madeiramadeira(websocket, path):
    query = await websocket.recv() #recives from client

    target = urllib.request.urlopen('https://www.madeiramadeira.com.br/busca?q=' + query ).read()
    soup = BeautifulSoup(target, "html.parser")
    limit = 20
    i = 0
    for item in soup.select('div.col-xs-4.no-padding'):
        product = item.find('div','product-box__item')
        if product is not None and i < limit:
            i += 1
            store = "MAD"
            link = product.find("div","product__image").find("a")["href"]
            link = "https://www.madeiramadeira.com.br" + link
            title = product.find("div","product__name").find("a")["title"]
            image = product.find("div","product__image").find("div","product-wishlist").find("button","product-wishlist__button")["data-wishlist-button-variation-img"]
            price = product.find("div","product__summary").find("span","text text--default text--block").find("span","text--large text--highlight text--semibold").get_text().replace("/m","").replace("\n","").replace("   ","")
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

start_server = websockets.serve(scrap_madeiramadeira, "localhost", 8767)

try:
    print('starting madeira-madeira')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except:
    print('Erro: trying to start madeira-madeira')