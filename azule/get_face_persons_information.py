import requests

def get_person_information():
    request = requests.get(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/persons',
        headers = {
            'Ocp-Apim-Subscription-Key': '******'
        }
        
    )
    print(request.json())

get_person_information()
