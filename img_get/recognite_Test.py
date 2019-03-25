
# coding: utf-8

# In[5]:


# -*- coding: utf-8 -*-

import cv2
import os

#HAAR分類器の顔検出用の特徴量
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "haarcascade_frontalface_alt.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
#cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml"

two_bitetest_str = "永瀬　蓮"
print (two_bitetest_str)
image_path = "/home/worker/collection-Johnnys/hirate/imgs/10b9c320385575e625803f2ff037a7fe2548a036ad8d241a9a2e5222b356a54d.jpg"
#image_path = "/home/worker/collection-Johnnys/jr_images/" + two_bitetest_str + "/imgs/2fc62cdc327eb81ed488acd4ba5d8c650a9a681e7fc9fa34e0fa14565108d5af.jpg"
print(image_path)


color = (255, 255, 255) #白
#color = (0, 0, 0) #黒

#ファイル読み込み
image = cv2.imread(image_path)
print(image_path)
#グレースケール変換
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path)

#物体認識（顔認識）の実行
#image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
#objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
#scaleFactor – 各画像スケールにおける縮小量を表します
#minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
#flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
#minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
#facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

print ("face rectangle")
print (facerect)
face_recognize_num =0
if len(facerect) > 0:
    #検出した顔を囲む矩形の作成
    for rect in facerect:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
        
    for (x,y,w,h) in facerect:
                    dst = image[y:y+h, x:x+w]
                    resize_img = cv2.resize(dst, (64,64))
                    save_res_path = os.path.join('test') + '/' + str(face_recognize_num) + '.jpg'
                    cv2.imwrite(save_res_path, resize_img)
                    print(save_res_path)
                    face_recognize_num += 1
    #認識結果の保存
    cv2.imwrite("detected.jpg", image)

