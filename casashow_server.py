import cgitb
import json
import urllib.request #get the html from url
import asyncio
import websockets

from bs4 import BeautifulSoup # 

cgitb.enable

async def scrap_casashow(websocket, path):
    query = await websocket.recv() #recives from client

    target = urllib.request.urlopen( 'https://www.casashow.com.br/' + query ).read()
    soup = BeautifulSoup( target, "html.parser" )
    for product in soup.select('div.prateleira__item'):
        price = product.find( "span", "prateleira__best-price" )
        if price is not None:
            store = "CSH"
            link = product.find('a','prateleira__name')["href"]
            title = product[ "title" ]
            image = product.find('div','prateleira__image imagem-principal').find("img")["src"]
            price = price.get_text().replace("R$","").replace(" ","")
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

start_server = websockets.serve(scrap_casashow, "localhost", 8768)

try:
    print('starting casa-show')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except:
    print('Erro: trying to start casa-swhow')