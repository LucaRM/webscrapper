import cgitb
import urllib.request #get the html from url
import asyncio
import websockets

from bs4 import BeautifulSoup  

cgitb.enable

async def scrap_cec(websocket, path): 
    query = await websocket.recv() #recives from client

    target = urllib.request.urlopen('http://www.cec.com.br/busca?q='+ query + '&resultsperpage=50').read()
    soup = BeautifulSoup(target, "html.parser")
    for item in soup.select('div[id*="divShowcaseProduct_"]'):
        store = "CEC"
        link = item.find("div", "product").find("a", "photo")["href"]
        link = "http://www.cec.com.br" + link
        title = item.find("div", "product").find("a", "name-and-brand").find( "span" ).get_text()
        image = item.find("div", "product").find("a", "photo").find("img")["src"]
        #preco_unav = item.find("div", "product").find("a", "price-and-offers").find( "b" )
        #if preco_unav is None:
        preco = item.find("div", "product").find("a", "price-and-offers").find( "span", "price" ).find( "meta" ).findNext( "meta" )[ "content" ]
        await websocket.send(preco) #send to client
        brand = item.find("div", "product").find("a", "name-and-brand").find( "span" ).findNext("span").get_text().strip()[2:]
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

start_server = websockets.serve(scrap_cec, "localhost", 8770)

try:
    print('starting cec')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except:
    print('Erro: trying to start cec')