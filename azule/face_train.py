import requests

def train_FaceGroup():
    request = requests.post(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/train',
        headers = {
            'Ocp-Apim-Subscription-Key': '*****'
        },
        json = {'personGroupId':'johnnys_jr'}
    )
    print(request.text)
train_FaceGroup()
