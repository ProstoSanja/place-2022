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
    try:
        r = requests.post(f'https://www.reddit.com/api/v1/access_token?grant_type=password&username={authparams.USERNAME}&password={authparams.PASSWORD}',
                    auth=HTTPBasicAuth(authparams.OAUTH_CLIENT, authparams.OAUTH_SECRET))
        auth_response = json.loads(r.text)
        return auth_response['access_token']
    except:
        return auth_token

currentConfig = {}
timeat = 0
big_error = False

def on_message(ws, message):
    global big_error
    payload = json.loads(message)
    if payload['type'] == "connection_error":
        big_error = True
        ws.close()
        return
    if payload['type'] != "data":
        return
    if payload['payload']['data']['subscribe']['data']['__typename'] == "ConfigurationMessageData":
        messageIndex = 2
        canvasConfig = payload['payload']['data']['subscribe']['data']['canvasConfigurations']
        canvasHeight = payload['payload']['data']['subscribe']['data']['canvasHeight']
        canvasWidth = payload['payload']['data']['subscribe']['data']['canvasWidth']
        activeZoneRaw = payload['payload']['data']['subscribe']['data']['activeZone']
        activeZone = {
            "startX": activeZoneRaw['topLeft']['x'],
            "startY": activeZoneRaw['topLeft']['y'],
            "endX": activeZoneRaw['bottomRight']['x'],
            "endY": activeZoneRaw['bottomRight']['y']
        }
        for configItem in canvasConfig:
            if configItem['__typename'] == "CanvasConfiguration":
                itemIndex = configItem['index']
                currentConfig[itemIndex] = {
                    "url": None,
                    "completed": False,
                    "startX": configItem['dx'],
                    "startY": configItem['dy'],
                    "endX": configItem['dx'] + canvasWidth,
                    "endY": configItem['dy'] + canvasHeight
                }
                if (currentConfig[itemIndex]["endX"] <= activeZone["startX"] or currentConfig[itemIndex]["startX"] >= activeZone["endX"]):
                    currentConfig[itemIndex]['completed'] = True
                if (currentConfig[itemIndex]["endY"] <= activeZone["startY"] or currentConfig[itemIndex]["startY"] >= activeZone["endY"]):
                    currentConfig[itemIndex]['completed'] = True
        for index in currentConfig.keys():
            if (not currentConfig[index]['completed']):
                ws.send('{"id":"' + str(messageIndex) + '","type":"start","payload":{"variables":{"input":{"channel":{"teamOwner":"GARLICBREAD","category":"CANVAS","tag":"' + str(index) +'"}}},"extensions":{},"operationName":"replace","query":"subscription replace($input:SubscribeInput!){subscribe(input:$input){id...on BasicMessage{data{__typename...on FullFrameMessageData{__typename name timestamp}...on DiffFrameMessageData{__typename name currentTimestamp previousTimestamp}}__typename}__typename}}"}}')
                messageIndex += 1

    if payload['payload']['data']['subscribe']['data']['__typename'] == "FullFrameMessageData":
        url = payload['payload']['data']['subscribe']['data']['name']
        extractedIndex = int(re.search("[0-9]{13}-([0-9]{1})", url).group(1))
        currentConfig[extractedIndex]['url'] = url
        fetchImageFromUrl(url, extractedIndex, ws)

def fetchImageFromUrl(url, index, ws):
    response = requests.get(url)
    filename = "images2/" + str(index) + "-" + str(timeat) + '.png'
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
    ws.send('{"id":"1","type":"start","payload":{"variables":{"input":{"channel":{"teamOwner":"GARLICBREAD","category":"CONFIG"}}},"extensions":{},"operationName":"configuration","query":"subscription configuration($input:SubscribeInput!){subscribe(input:$input){id...on BasicMessage{data{__typename...on ConfigurationMessageData{colorPalette{colors{hex index __typename}__typename}canvasConfigurations{index dx dy __typename}activeZone{topLeft{x y __typename}bottomRight{ x y __typename} __typename}canvasWidth canvasHeight __typename}}__typename}__typename}}"}}')

if __name__ == "__main__":
    while True:
        try:
            currentConfig = {}
            timeat = int(time.time())
            ws = websocket.WebSocketApp("wss://gql-realtime-2.reddit.com/query",
                                    on_message=on_message,
                                    on_open=on_open)
            ws.run_forever()
            if big_error:
                big_error = False
                raise "ERROR"
        except Exception as ex:
            auth_token = auth()
            print("ERROR")

        time.sleep(30)