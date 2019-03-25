import requests
import json

def detectFace(imageUrl):
    img_data = open(imageUrl,'rb').read()
    result = requests.post(
    'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect',
    headers = {
        'Ocp-Apim-Subscription-Key': '****',
        'Content-Type': 'application/octet-stream'
        },
    data = img_data
    )
    print(result.json())
    return json.loads(result.text)[0]['faceId']
def identifyPerson(detectdFaceId):
    result = requests.post(
    'https://eastus.api.cognitive.microsoft.com/face/v1.0/identify',
    headers = {
            'Ocp-Apim-Subscription-Key':'****'
            },
    json = {
        'faceIds': [detectedFaceId],
        'personGroupId': 'johnnys_jr'
    }
    )
    identifiedPerson = json.loads(result.text)[0]['candidates']
    return identifiedPerson

def getPersonNameByPersonId(personId):
    result = requests.get(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/persons',
    headers = {'Ocp-Apim-Subscription-Key':'******'
            },
    json = {
        'personGroupId': 'johnnys_jr'
    }
    )
    persons = json.loads(result.text)
    #print(persons)
    for person in persons:
        #print(person)
        if person['personId'] == personId:
            return person['name']
targetFile = '00000012.jpg'
detectedFaceId = detectFace(targetFile)
identifiedPerson = identifyPerson(detectedFaceId)
print(identifiedPerson)
identifiedPersonName = getPersonNameByPersonId(identifiedPerson[0]["personId"])
print(identifiedPersonName)
