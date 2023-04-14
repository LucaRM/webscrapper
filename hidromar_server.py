import cgitb
import urllib.request #get the html from url
import asyncio
import websockets

from bs4 import BeautifulSoup  

cgitb.enable

async def scrap_hidromar(websocket, path): 
    query = await websocket.recv() #recives from client

    target = urllib.request.urlopen('https://www.lojashidromar.com.br/procurar?controller=search&order=product.position.desc&s=' + query).read()
    soup = BeautifulSoup(target, "html.parser")

    for item in soup.select("article.product-miniature"):
        price = item.find("div","product-description").find("div","product-price-and-shipping").find("span")
        if price is not None:
            store = "HID"
            link = item.find("div","product-description").find("h3","h3 product-title").find("a")["href"]
            title = item.find("h3","h3 product-title").get_text().replace("\n","")
            image = item.find("div","thumbnail-container").find("a").find("img")["data-src"]
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


start_server = websockets.serve(scrap_hidromar, "localhost", 8769)

try:
    print('starting hidromar')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except:
    print('Erro: trying to start hidromar')