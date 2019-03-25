import requests
import csv
import os
import time
def addFace(personId, imageUrl):
    img_data = open(imageUrl,'rb').read()
    response = requests.post(
    'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/persons/' + personId + '/persistedFaces',
    headers = {
        'Ocp-Apim-Subscription-Key': '*****',
        'Content-Type': 'application/octet-stream' 
    },
    data = img_data
        
    )
    print(response.json())
# personId # createPerson()で得られたpersonId
# imageUrl # personの画像url personその人しか写っていないものでないと、エラーになる
# pictures = [imageUrl, imageUrl, imageUrl......]
csva = []
with open('jr_personID.csv','rt') as fin:
    cin  = csv.reader(fin)
    csva = [row for row in cin]
    for row in csva:
        print(row[2],row[1])
for row in csva:
    image_path = os.path.join("jr_images", row[2],"cutted")
    for root, dir, files in os.walk(image_path):
        for file in files:
            print(row[1],os.path.join(image_path,file))
            addFace(row[1], os.path.join(image_path, file))
            time.sleep(3)
