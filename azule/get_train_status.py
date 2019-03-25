import requests

def get_train_status():
    request =  requests.get(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/training',
        headers = {
             'Ocp-Apim-Subscription-Key': '****'
        },
        json = {'personGroupId':'johnnys_jr'}
    )
    print(request.json())

get_train_status()

