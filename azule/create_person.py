import os
import pandas as pd
import csv
import shutil
import requests
import json
import time
df = pd.DataFrame()
def csv_to_dict(file_path):
    name_list = []
    name_dict = {}
    with open(file_path) as f:
        for tmp_line in csv.reader(f):
            name_dict[tmp_line[2]] = tmp_line[3]
    
    return name_dict

def createPerson(personName):
    result = requests.post(
        'https://eastus.api.cognitive.microsoft.com/face/v1.0/persongroups/johnnys_jr/persons',
        headers = {
            'Ocp-Apim-Subscription-Key': '****'
        },
        json = {
            'name': personName
        }
    )
    print(result)
    personId = json.loads(result.text)['personId'] # personのidを抽出できる
    return personId

file_path = 'jr_csv.csv'
dict = csv_to_dict(file_path)
print(dict.keys())
print(dict.items())
for value in dict.values():
    print(value)
    person_id = createPerson(value)
    series = pd.Series([value, person_id],["person_name", "person_id"])
    print(value, person_id)
    df = df.append(series, ignore_index=True )
    time.sleep(5)

df.to_csv("jr_personID.csv")
print("finished")
     
