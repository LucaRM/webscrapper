""" CDO WebScrapper """
import threading
import cgi
# import xml.etree.ElementTree as ET
import cgitb
# import re
import json
# import requests
# import cookiejar
# import itertools
# import urllib.request
import asyncio
# import pathlib
# import ssl
import websockets
import time
import threading


from bs4 import BeautifulSoup

cgitb.enable

print ("Content-Type: text/html\n\n")

form = cgi.FieldStorage()

#MultiThreading class
class wss_thread(threading.Thread):
    def __init__(self,threadID, name, query):#atributes
        #setting vars
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.query = query

    def run(self):
        print (f"Starting {self.name}")
        
        #start telha-norte
        if self.threadID == 1:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop.run_until_complete(scrap_telhanorte('ws://localhost:8765',self.query)))
        
        #start gimawa
        elif self.threadID == 2:
            lis = ['tijolo','tinta'] #gimawa hasn't these products in his store
            if self.query not in lis:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop.run_until_complete(scrap_gimawa('ws://localhost:8766',self.query)))

        #start madeira-madeira
        elif self.threadID == 3:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop.run_until_complete(scrap_madeiramadeira('ws://localhost:8767',self.query)))

        #start casa-show
        elif self.threadID == 4: 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop.run_until_complete(scrap_casashow('ws://localhost:8768',self.query)))
        
        #start hidromar
        elif self.threadID == 5: 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop.run_until_complete(scrap_hidromar('ws://localhost:8769',self.query)))

        #start cec
        elif self.threadID == 6: 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop.run_until_complete(scrap_cec('ws://localhost:8770',self.query)))

        print (f"Exiting {self.name}")


#creta an array
def array(x,y):
    a = [None]*x
    for i in range(len(a)):
        a[i] = [0]*y
    for  i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = 0
    return a

#if there is 0 in an array, delete it
def verify(a):
  while True:
    if a[-1][0] == 0:
      a.pop(-1)
    else:
      return a

#----------------------------------------------------------------------------------------------------------------------------------------------------#

if form and "comparar" in form.keys():                                      # check if comparar is the same as the form
    result = []

    async def scrap_telhanorte(uri,query):                                  # create the function that make connection with server
        #uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:                    # make the connection
            await websocket.send(query)                                     # send the query for the function in the server
            lin = array(10,6)
            for i in range(len(lin)):
                for j in range(len(lin[0])):
                    lin[i][j] = await websocket.recv()                      # recives from server and store in an array
            verify(lin)                                                     # check the array
            result.append(lin)
            print ('telha norte:',len(lin))


    async def scrap_gimawa(uri,query):                                      # create the function that make connection with server
        #uri = "ws://localhost:8766"
        async with websockets.connect(uri) as websocket:                    # make the connection
            await websocket.send(query)                                     # send the query for the function in the server
            lin = array(10,6)
            for i in range(len(lin)):
                for j in range(len(lin[0])):
                    lin[i][j] = await websocket.recv()                      # recives from server and store in an array
            verify(lin)                                                     # check the array
            result.append(lin)
            print ('gimawa:',len(lin))


    async def scrap_madeiramadeira(uri,query):                              # create the function that make connection with server
        #uri = "ws://localhost:8767"
        async with websockets.connect(uri) as websocket:                    # make the connection
            await websocket.send(query)                                     # send the query for the function in the server
            lin = array(10,6)
            for i in range(len(lin)):
                for j in range(len(lin[0])):
                    lin[i][j] = await websocket.recv()                      # recives from server and store in an array
            verify(lin)                                                     # check the array
            result.append(lin)
            print ('madeiramadeira:',len(lin))


    async def scrap_casashow (uri,query):
        #uri = "ws://localhost:8768"
        async with websockets.connect(uri) as websocket:                    # make the connection
            await websocket.send(query)                                     # send the query for the function in the server
            lin = array(10,6)
            for i in range(len(lin)):
                for j in range(len(lin[0])):
                    lin[i][j] = await websocket.recv()                      # recives from server and store in an array
            verify(lin)                                                     # check the array
            result.append(lin)
            print ('casa-show:',len(lin))


    async def scrap_hidromar (uri,query):
        #uri = "ws://localhost:8769"
        async with websockets.connect(uri) as websocket:                    # make the connection
            await websocket.send(query)                                     # send the query for the function in the server
            lin = array(10,6)
            for i in range(len(lin)):
                for j in range(len(lin[0])):
                    lin[i][j] = await websocket.recv()                      # recives from server and store in an array
            verify(lin)                                                     # check the array
            result.append(lin)
            print ('hidromar:',len(lin))


    async def scrap_cec (uri,query):
        #uri = "ws://localhost:8770"
        async with websockets.connect(uri) as websocket:                    # make the connection
            await websocket.send(query)                                     # send the query for the function in the server
            lin = array(10,6)
            for i in range(len(lin)):
                for j in range(len(lin[0])):
                    lin[i][j] = await websocket.recv()                      # recives from server and store in an array
            verify(lin)                                                     # check the array
            result.append(lin)
            print ('cec:',len(lin))


    #------------------------------main-------------------------------------#
    # Create new threads
    telha = wss_thread(1,'telha-norte',(form['comparar'].value).lower())
    gim = wss_thread(2,'gimawa',(form['comparar'].value).lower())
    mad = wss_thread(3,'madeira-madeira',(form['comparar'].value).lower())
    casa = wss_thread(4,'casa-show',(form['comparar'].value).lower())
    hid = wss_thread(5,'hidromar',(form['comparar'].value).lower())
    cec = wss_thread(6,'cec',(form['comparar'].value).lower())

    # Start new Threads
    telha.start()       #.start() - call run() function
    gim.start()
    mad.start()
    casa.start()
    hid.start()
    cec.start()

    print()

    telha.join()        #.join() - start the threading
    gim.join()
    mad.join()
    casa.join()
    hid.join()
    cec.join()
    #print(result)
    print ("Exiting Main Thread")
