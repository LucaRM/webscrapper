import cgitb
import json
import urllib.request #get the html from url
import asyncio
import websockets

from bs4 import BeautifulSoup # 

cgitb.enable

async def scrap_gimawa( websocket, path ):
    #this scrap with 'luz', return 60 items

    query = await websocket.recv() #recives from client
    query = query.replace("-","+")

    target = urllib.request.urlopen('https://www.gimawa.com/com_consulta_produto.aspx?TipCon=BP&CHR_TIPBUS=O&CATP_COD=-1&STACOM=TO|-1&NOM_BUS='+query).read()
    soup = BeautifulSoup(target, "html.parser")
    item = soup.find('span','cvProduto')
    #if item == None:
    #    await websocket.close()
    for item in soup.select("span.cvProduto"):
        price = item.find("span","divPrecos_consulta")
        if price is not None:
            store = "GIM"
            link = item.find("center").find("a")["href"]
            title = item.find("a","prodNom").find("strong").get_text().replace("\n", "").replace("\t", "").strip()
            image = item.find("center").find("a").find("img")["data-original"]
            price = price.get_text().replace("R$ ", "").replace("por","").replace(",", "").replace(".", ",").strip() 
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


start_server = websockets.serve(scrap_gimawa, "localhost", 8766)

try:
    print('starting gimawa')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except:
    print('Erro: trying to start gimawa')