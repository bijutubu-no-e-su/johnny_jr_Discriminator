import cognitive_face as CF
import json

def main():
    # APIキーのセット
    api_key = '***'
    CF.Key.set(api_key)
    BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/' 
    CF.BaseUrl.set(BASE_URL)
    
    print(api_key)
    # Person Groupの作成
    GroupId = 'johnnys_jr'
    GroupName = 'johnnys_jr'
    CF.person_group.create(GroupId, name=GroupName)
    # Person Groupの確認
    print(json.dumps(CF.person_group.get(GroupId), indent = 4))
    
if __name__ == '__main__':
    main()
