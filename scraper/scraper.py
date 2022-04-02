import websocket
import json
import requests
import time
import re
import os
from requests.auth import HTTPBasicAuth

import authparams

auth_token = authparams.AUTH_TOKEN
def auth():
    r = requests.post(f'https://www.reddit.com/api/v1/access_token?grant_type=password&username={authparams.USERNAME}&password={authparams.PASSWORD}',
                  auth=HTTPBasicAuth(authparams.OAUTH_CLIENT, authparams.OAUTH_SECRET))
    auth_response = json.loads(r.text)
    try:
        return auth_response['access_token']
    except:
        return auth_token

currentConfig = {}
timeat = 0

def on_message(ws, message):
    payload = json.loads(message)
    if payload['type'] != "data":
        return
    if payload['payload']['data']['subscribe']['data']['__typename'] == "ConfigurationMessageData":
        messageIndex = 2
        canvasConfig = payload['payload']['data']['subscribe']['data']['canvasConfigurations']
        for configItem in canvasConfig:
            if configItem['__typename'] == "CanvasConfiguration":
                itemIndex = configItem['index']
                currentConfig[itemIndex] = {
                    "url": None,
                    "completed": False,
                }
        for index in currentConfig.keys():
            ws.send('{"id":"' + str(messageIndex) + '","type":"start","payload":{"variables":{"input":{"channel":{"teamOwner":"AFD2022","category":"CANVAS","tag":"' + str(index) +'"}}},"extensions":{},"operationName":"replace","query":"subscription replace($input:SubscribeInput!){subscribe(input:$input){id...on BasicMessage{data{__typename...on FullFrameMessageData{__typename name timestamp}...on DiffFrameMessageData{__typename name currentTimestamp previousTimestamp}}__typename}__typename}}"}}')
            messageIndex += 1

    if payload['payload']['data']['subscribe']['data']['__typename'] == "FullFrameMessageData":
        url = payload['payload']['data']['subscribe']['data']['name']
        extractedIndex = int(re.search("[0-9]{13}-([0-9]{1})", url).group(1))
        currentConfig[extractedIndex]['url'] = url
        fetchImageFromUrl(url, extractedIndex, ws)

def fetchImageFromUrl(url, index, ws):
    response = requests.get(url)
    filename = "images\\" + str(index) + "-" + str(timeat) + '.png'
    open(os.path.join(os.path.dirname(__file__), filename), 'wb').write(response.content)
    currentConfig[index]['completed'] = True
    print(f'Fetched {str(index)}', end=' ')
    for configItem in currentConfig.values():
        if (not configItem['completed']):
            return
    print(f'All fetched at: {str(timeat)}')
    ws.close()



def on_open(ws):
    ws.send('{"type":"connection_init","payload":{"Authorization":"Bearer ' + auth_token + '"}}')
    ws.send('{"id":"1","type":"start","payload":{"variables":{"input":{"channel":{"teamOwner":"AFD2022","category":"CONFIG"}}},"extensions":{},"operationName":"configuration","query":"subscription configuration($input:SubscribeInput!){subscribe(input:$input){id...on BasicMessage{data{__typename...on ConfigurationMessageData{colorPalette{colors{hex index __typename}__typename}canvasConfigurations{index dx dy __typename}canvasWidth canvasHeight __typename}}__typename}__typename}}"}}')

if __name__ == "__main__":
    while True:
        try:
            currentConfig = {}
            timeat = int(time.time())
            ws = websocket.WebSocketApp("wss://gql-realtime-2.reddit.com/query",
                                    on_message=on_message,
                                    on_open=on_open)
            ws.run_forever()
        except:
            auth_token = auth()
            print("ERROR")

        time.sleep(30)