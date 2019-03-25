
# coding: utf-8

# In[3]:


from requests import exceptions
import argparse
import requests
import cv2
import os
import pandas as pd
from joblib import Parallel, delayed

#パラメタ設定値
API_KEY = "*******"
MAX_RESULTS = 20
GROUP_SIZE = 10
# 取得したエンドポイントURL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
#ファイル出力先
PARENT_OUTPUT = '*****'
INPUT = 'jr_csv.csv'
def get_image_by_bing_api(headers,params,OUTPUT):
    EXCEPTIONS = set([IOError, FileNotFoundError,
    exceptions.RequestException, exceptions.HTTPError,
    exceptions.ConnectionError, exceptions.Timeout, exceptions.SSLError])
    
    # make the search
    print("[INFO] searching Bing API for '{}'".format(params["q"]))
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()

    # grab the results from the search, including the total number of
    # estimated results returned by the Bing API
    results = search.json()
    #画像取得ができなかったとき
    if results.get("totalEstimatedMatches") == None:
        print("[INFO] Nothing results for '{}' ".format(params["q"]))
        return 
        
    
    estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)

    print("[INFO] {} total results for '{}'".format(estNumResults,params["q"]))

    # initialize the total number of images downloaded thus far
    total = 0

    # loop over the estimated number of results in `GROUP_SIZE` groups
    for offset in range(0, estNumResults, GROUP_SIZE):
        # update the search parameters using the current offset, then
        # make the request to fetch the results
        print("[INFO] making request for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
        params["offset"] = offset
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()
        print("[INFO] saving images for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
        # loop over the results
        for v in results["value"]:
        # try to download the image
            try:
                # make a request to download the image
                print("[INFO] fetching: {}".format(v["contentUrl"]))
                r = requests.get(v["contentUrl"], timeout=30)

                # build the path to the output image
                print
                ext = v["contentUrl"][v["contentUrl"].rfind("."):v["contentUrl"].rfind("?") if v["contentUrl"].rfind("?") > 0 else None]
                p = os.path.sep.join([OUTPUT, "{}{}".format(str(total).zfill(8), ext)])
                
                # write the image to disk
                f = open(p, "wb")
                f.write(r.content)
                f.close()
            # catch any errors that would not unable us to download the
            # image
            except Exception as e:
                # check to see if our exception is in our list of
                # exceptions to check for
                print("[INFO]:exception occur",e)
                if type(e) in EXCEPTIONS:
                    print("[INFO] skipping: {}".format(v["contentUrl"]))
                    continue
            # try to load the image from disk
            print("[INFO] p = {}", p)
            image = cv2.imread(p)


            # if the image is `None` then we could not properly load the
            # image from disk (so it should be ignored)
            if image is None:
                print("[INFO] deleting: {}".format(p))
                os.remove(p)
                continue
            # update the counter
            total += 1
    
# 2CPUで並列化
#Parallel(n_jobs=2)([delayed(get_image_by_bing_api)(offset) for offset in range(0, estNumResults, GROUP_SIZE)])

def csv_to_name_Series(file_path):
    name_list = []
    name_df = pd.read_csv(file_path)
    for name in name_df["name"]:
        name_list.append(name)
    return name_list

def mkdir_for_member(name_dir):
    if not os.path.isdir(name_dir):
        os.mkdir(name_dir)
    
#APIのためのパラメタ設定
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": "", "offset": 0, "count": GROUP_SIZE, "imageType":"Photo", "color":"ColorOnly"}

#csvより名前のリストを取得
name_list = csv_to_name_Series(INPUT)

for name in name_list:
    name_dir = os.path.join(PARENT_OUTPUT, name)
    mkdir_for_member(name_dir)
    params["q"] = name
    get_image_by_bing_api(headers,params,name_dir)

print("finished saving")
    

