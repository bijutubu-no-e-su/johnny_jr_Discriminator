
# coding: utf-8

# In[29]:


#-*- coding:utf-8 -*-
import urllib.request
import httplib2
import json
import os
import pickle
import hashlib
import sys
import pandas as pd

from googleapiclient.discovery import build


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def make_correspondence_table(correspondence_table, original_url, hashed_url):
    correspondence_table[original_url] = hashed_url


def getImageUrl(api_key, cse_key, search_word, page_limit, save_dir_path):

    service = build("customsearch", "v1", developerKey=api_key)
    page_limit = page_limit
    startIndex = 1
    response = []

    img_list = []

    make_dir(save_dir_path)
    save_res_path = os.path.join(save_dir_path, 'api_response_file')
    make_dir(save_res_path)

    for nPage in range(0, page_limit):
        print("Reading page number:", nPage + 1)

        try:
            response.append(service.cse().list(
                q=search_word,     # Search words
                cx=cse_key,        # custom search engine key
                lr='lang_ja',      # Search language
                num=10,            # Number of images obtained by one request (Max 10)
                start=startIndex,
                searchType='image' # search for images
            ).execute())

            startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")

        except Exception as e:
            print(e)

    with open(os.path.join(save_res_path, 'api_response.pickle'), mode='wb') as f:
        pickle.dump(response, f)

    for one_res in range(len(response)):
        if len(response[one_res]['items']) > 0:
            for i in range(len(response[one_res]['items'])):
                img_list.append(response[one_res]['items'][i]['link'])
    
    
    return img_list


def getImage(save_dir_path, img_list):
    make_dir(save_dir_path)
    save_img_path = os.path.join(save_dir_path, 'imgs')
    make_dir(save_img_path)

    opener = urllib.request.build_opener()
    http = httplib2.Http(".cache")

    for i in range(len(img_list)):
        try:
            url = img_list[i]
            extension = os.path.splitext(img_list[i])[-1]
            
            if extension.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):
                encoded_url = url.encode('utf-8')  # required encoding for hashed
                a = hashlib.sha3_224()
                
                hashed_url = hashlib.sha3_256(encoded_url).hexdigest()
                full_path = os.path.join(save_img_path, hashed_url + extension.lower())

                response, content = http.request(url)
                with open(full_path, 'wb') as f:
                    f.write(content)
                print('saved image... {}'.format(url))

                make_correspondence_table(correspondence_table, url, hashed_url)

        except Exception as e:
            print(e)
            print("failed to download images.")
            continue
def csv_to_name_Series(file_path):
    name_list = []
    name_df = pd.read_csv(file_path)
    for name in name_df["name"]:
        name_list.append(name)
    return name_list

def mkdir_for_member(name_dir):
    if not os.path.isdir(name_dir):
        os.mkdir(name_dir)

if __name__ == '__main__':
    # -------------- Parameter and Path Settings -------------- #
    API_KEY = '****'
    #CUSTOM_SEARCH_ENGINE = '003255470133039666796:yaeh4_ineay'
    INPUT = 'jr_csv.csv'
    PARENT_OUTPUT = '/home/worker/collection-Johnnys/jr_images'
    #csvより名前のリストを取得
    name_list = csv_to_name_Series(INPUT)
    page_limit = 10
    
    

    correspondence_table = {}
    
    for name in name_list:
        search_word = name
        save_dir_path = os.path.join(PARENT_OUTPUT, name)
        print("[INFO]:searching  searching Google API for '{}'" ,name)
        img_list = getImageUrl(API_KEY, CUSTOM_SEARCH_ENGINE, search_word, page_limit, save_dir_path)
        getImage(save_dir_path, img_list)

        correspondence_table_path = os.path.join(save_dir_path, 'corr_table')
        make_dir(correspondence_table_path)

        with open(os.path.join(correspondence_table_path, 'corr_table.json'), mode='w') as f:
            json.dump(correspondence_table, f)

