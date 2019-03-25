
# coding: utf-8

# In[ ]:


import os
import cv2
import pandas as pd

imageFileDir = 'imgs'
membersDir = 'jr_images'
jr_csv = 'jr_csv.csv'
def mkdir_for_member(name_dir):
    if not os.path.isdir(name_dir):
        os.mkdir(name_dir)

def cuttingFace_resize(target_dir,imageFile_List,save_Dir):
    color = (255, 255, 255)
    cascade_path = "haarcascade_frontalface_alt.xml"
    face_recognize_num =0
    for imageFile in imageFile_List:
        print(os.path.join(target_dir,imageFile))
        image = cv2.imread(os.path.join(target_dir,imageFile))
        if image is None:
            continue
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #カスケード分類器の特徴量を取得する
        cascade = cv2.CascadeClassifier(cascade_path)
        facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
        
        if len(facerect) > 0:
            for (x,y,w,h) in facerect:
                    dst = image[y:y+h, x:x+w]
                    resize_img = cv2.resize(dst, (64,64))
                    save_res_path = save_Dir +'/'+ str(face_recognize_num) + '.jpg'
                    cv2.imwrite(save_res_path, resize_img)
                    print(save_res_path)
                    face_recognize_num += 1

jr_pd = pd.read_csv('jr_csv.csv')
name_series = jr_pd['name_alphabet']
#print(name_series)
for name in name_series:
        print(name)
        save_Dir = os.path.join(membersDir,name,'cutted')
        mkdir_for_member(save_Dir)
        target_dir = os.path.join(membersDir,name,imageFileDir)
        imageFile_List = os.listdir(target_dir)
        cuttingFace_resize(target_dir,imageFile_List,save_Dir)

