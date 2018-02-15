#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys
import glob
import csv
import requests
import json
import shutil

from constants.api_keys import KEY_SLACK
from constants.learning_meta import SEARCH_DIR
from constants.learning_meta import LIKELI_DIR
from constants.learning_meta import IMG_PATH

from constants.learning_meta import THRESHOLD

img_paths = glob.glob(SEARCH_DIR+"*")

score_lists = []

for img_path2 in img_paths:
  img1 = cv2.imread(IMG_PATH)
  img2 = cv2.imread(img_path2)

  # 特徴量記述
  detector = cv2.AKAZE_create()
  #detector = cv2.xfeatures2d.SIFT_create()
  kp1, des1 = detector.detectAndCompute(img1, None)
  kp2, des2 = detector.detectAndCompute(img2, None)
  
  # 比較器作成
  bf = cv2.BFMatcher(cv2.NORM_HAMMING)
  #bf = cv2.BFMatcher()
  
  # 画像への特徴点の書き込み
  matches = bf.knnMatch(des1, des2, k=2)
  
  good_score = []
  for m,n in matches:
    if m.distance < THRESHOLD * n.distance:
      good_score.append([m])
  
  filename = img_path2.replace(SEARCH_DIR, "")  
  c_score = len(good_score)

  score_list = []
  score_list.append(filename)
  score_list.append(c_score)
  score_lists.append(score_list)

#result_csv = open("result.csv", "a")
#writer = csv.writer(result_csv, lineterminator="\n")
#writer.writerows(score_lists)

sorted_list = sorted(score_lists, key=lambda x:x[1], reverse=True)
extracted_range = int(len(img_paths)/10)

for candidates in sorted_list[:extracted_range]:
    print(SEARCH_DIR+candidates[0])
    shutil.copy(SEARCH_DIR+candidates[0],LIKELI_DIR+candidates[0])

url = "https://hooks.slack.com/services/" + KEY_SLACK
requests.post(url, data=json.dumps({
    'username': "endnotifier",
    'link_names': 1,
    'attachments': [{
        "text": u"最大値は"+sorted_list[0][0]+"の"+str(sorted_list[0][1])+"デス^^)",
    }]
}))
