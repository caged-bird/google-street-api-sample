#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys
import glob
import csv
import requests
import json
from const import get_slack_key

THRESHOLD = 0.8
DIR = "search_image/"

img_paths = glob.glob(DIR+"*")
IMG_PATH = "ref_image/namehouse.jpg"

score_lists = []
max_score = 0
max_list = []

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
  #matches = bf.match(des1, des2)
  matches = bf.knnMatch(des1, des2, k=2)
  
  good_score = []
  for m,n in matches:
    if m.distance < THRESHOLD * n.distance:
      good_score.append([m])
  
  filename = img_path2.replace(DIR, "")  
  c_score = len(good_score)

  score_list = []
  score_list.append(filename)
  score_list.append(c_score)
  score_lists.append(score_list)

  if c_score > max_score:
    max_score = c_score
    max_list = [filename, max_score]

result_csv = open("result.csv", "a")
writer = csv.writer(result_csv, lineterminator="\n")
writer.writerows(score_lists)

url = "https://hooks.slack.com/services/" + get_slack_key()
requests.post(url, data=json.dumps({
    'username': "endnotifier",
    'link_names': 1,
    'attachments': [{
        "text": u"最大値は"+max_list[0]+"の"+str(max_list[1])+"デス^^)",
    }]
}))
