import re
import lxml.html
from urllib.request import urlopen
import  pandas as pd
df = pd.DataFrame()
tree = lxml.html.parse(urlopen(''))
html = tree.getroot()
index = 1
for p in html.cssselect('p'):
    name = p.cssselect('strong > a')
    if name != []:
        member_name = name[0].text
        after_member_name = re.split("（" ,member_name)
        img = p.cssselect('img')
        if img != []:
            img_src = p.cssselect('img')[0].get('src')
            tmp_url = img_src.split('/').pop()
            name_alphabet =  tmp_url.split('.')[0][:-2]
        else:
            img_src = "no image"
        series = pd.Series([after_member_name[0], img_src,name_alphabet],["name", "image_url","name_alphabet"])
        df = df.append(series, ignore_index=True )
        print(index, member_name,  img_src,name_alphabet)
        index = index + 1

print(df.to_json("jr_json.json"))
df.to_csv("jr_csv.csv")
print("finished scraping")

