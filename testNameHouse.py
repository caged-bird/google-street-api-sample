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

    # FLANN parameters
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH,
                        table_number=6,
                        key_size=12,
                        multi_probe_level=1)
    search_params = dict(checks=50)

    # 特徴量記述
    detector = cv2.AKAZE_create()
    #detector = cv2.xfeatures2d.SURF_create()
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    # 比較器作成
    #bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    #bf = cv2.BFMatcher()
    bf = cv2.FlannBasedMatcher(index_params, search_params)

    # 画像への特徴点の書き込み
    matches = bf.knnMatch(des1, des2, k=2)

    good_score = []
    # m: 0 に近く
    # n: 大きくなる
    scores = []
    normal_matches = [match for match in matches if len(match) is 2]
    for i,[m,n] in enumerate(normal_matches):
        if m.distance < THRESHOLD * n.distance:
            good_score.append([m])
            scores.append([m])

    filename = img_path2.replace(SEARCH_DIR, "")
    c_score = len(good_score)

    score_list = []
    score_list.append(filename)
    score_list.append(c_score)
    score_list.append(scores[:50])
    score_list.append(kp1)
    score_list.append(kp2)
    score_lists.append(score_list)

result_csv = open("result.csv", "a")
writer = csv.writer(result_csv, lineterminator="\n")
writer.writerows(score_lists)

sorted_list = sorted(score_lists, key=lambda x:x[1], reverse=True)
extracted_range = int(len(img_paths)/2)

for candidates in sorted_list[:extracted_range]:
    print(SEARCH_DIR+candidates[0])
    shutil.copy(SEARCH_DIR+candidates[0],LIKELI_DIR+candidates[0])

    # 出力画像作成 表示

    img = cv2.imread(IMG_PATH)
    img2 = cv2.imread(SEARCH_DIR+candidates[0])

    h1, w1, c1 = img.shape[:3]
    h2, w2, c2 = img2.shape[:3]
    height = max([h1, h2])
    width = w1 + w2
    out = np.zeros((height, width, 3), np.uint8)

    match_image = cv2.drawMatchesKnn(img, candidates[3], img2, candidates[4], candidates[2], None, flags=2)
    cv2.imwrite(LIKELI_DIR+candidates[0], match_image)
