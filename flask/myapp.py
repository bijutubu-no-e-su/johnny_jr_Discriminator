# coding: utf-8
from flask import Flask
from flask import request
import logging
import logging.handlers 
import requests
import json
import re

import hmac
import hashlib
import base64

CHANNEL_ACCESS_TOKEN=''
CHANNEL_SECRET = ''

LINE_ENDPOINT = 'https://api.line.me/v2/bot'
app = Flask(__name__,static_folder='images_jr')

def detectFace(img_data):
    result = requests.post(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect',
        headers = {
            'Ocp-Apim-Subscription-Key': '',
            'Content-Type': 'application/octet-stream'
        },
    data = img_data
    )
    print(result.json())
    return json.loads(result.text)[0]['faceId']
    
def identifyPerson(detectedFaceId):
    result = requests.post(
    'https://eastus.api.cognitive.microsoft.com/face/v1.0/identify',
    headers = {
        'Ocp-Apim-Subscription-Key':''
        },
    json = {
        'faceIds': [detectedFaceId],
        'personGroupId': 'johnnys_jr',
        "confidenceThreshold": 0.1
    }
    )
    print(result.text)
    identifiedPerson = json.loads(result.text)[0]['candidates']
    print (identifiedPerson)
    return identifiedPerson

def getPersonNameByPersonId(personId):
    result = requests.get(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/persons',
    headers = {'Ocp-Apim-Subscription-Key':''
            },
    json = {
        'personGroupId': 'johnnys_jr'
    }
    )
    persons = json.loads(result.text)
    for person in persons:
        if person['personId'] == personId:
            return person['name']


def post(reply_token, messages):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
    }
    payload = {
            "replyToken": reply_token,
            "messages": messages,
    }
    print (header)
    print(json.dumps(payload))
    print(LINE_ENDPOINT+'/message/reply')
    
    print (requests.post(LINE_ENDPOINT+'/message/reply', headers=header, data=json.dumps(payload) ))
def get_profile(user_id):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
    }
    return json.loads(requests.get(LINE_ENDPOINT+'/profile/{}'.format(user_id), headers=header, data='{}' ).text)

def valdation_signature(signature, body):
    if isinstance(body, str) != True:
        body = body.encode()
    gen_signature = hmac.new(CHANNEL_SECRET.encode(), body.encode(), hashlib.sha256).digest()
    gen_signature = base64.b64encode(gen_signature).decode()

    if gen_signature == signature:
        return True
    else:
        return False

@app.route("/callback", methods=['POST'])
def callback():
    if valdation_signature(request.headers.get('X-Line-Signature', ''), request.data.decode()) == False:
        return 'Error: Signature', 403
    app.logger.info('CALLBACK: {}'.format(request.data))
    print (request.data)
    for event in request.json['events']:
        # follow
        if event['type'] == 'follow':
            if event['source']['type'] == 'user':
                profile = get_profile(event['source']['userId'])
            messages = [
                {
                    'type': 'text',
                    'text': 'thank you for adding me as a friend',
                },
                {
                    'type': 'text',
                    'text': 'HaHa',
                }
            ]
            if 'profile' in locals():
                messages[0]['text'] = '{}san\n'.format(profile['displayName'])+messages[0]['text']
            print (messages)
            post(event['replyToken'], messages)
            # Message
        elif event['type'] == 'message':
            if event['message']['type'] == 'image':
                header = {
                    "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN
                }
                contentId = event['message']['id']
                print(contentId)
                byteimage = requests.get(LINE_ENDPOINT+'/message/'+contentId+'/content',headers=header)
                print(byteimage)
                detectedFaceId = detectFace(byteimage)
                print(detectedFaceId)
                identifiedPerson = identifyPerson(detectedFaceId)
                print(identifiedPerson)
                identifiedPersonName = getPersonNameByPersonId(identifiedPerson[0]["personId"])
                print(identifiedPersonName)
                jr_url = identifiedPersonName + r'.jpg'
                print(jr_url)
                messages = [
                    {
                        'type': 'text',
                        'text': identifiedPersonName
                    },
                    {
                        'type':'image',
                        'originalContentUrl':'' + jr_url,
                        'previewImageUrl':'' + jr_url
                    }
                ]


                post(event['replyToken'], messages)
            elif event['message']['type'] == 'text':
                messages = [
                    {
                        'type': 'text',
                        'text': event['message']['text'],
                    },
                    {
                        'type': 'image',
                        'originalContentUrl':'',
                        'previewImageUrl':'',
                    }
                ]
                print (messages)
                print ('now sending...')
                post(event['replyToken'], messages)
                
        return '{}', 200

@app.route("/")
def hello():
    return "Flask."


if __name__ == "__main__":
    context = (fullchain.pem', 'privkey.pem')
    app.run(host='0.0.0.0',port=443,ssl_context = context, threaded=True,debug=True)
