#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys

img_path = "ref_image/namehouse.jpg"
img_path2 = "sample_image/namesample.jpg"

img = cv2.imread(img_path)
img2 = cv2.imread(img_path2)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 特徴量記述
detector = cv2.AKAZE_create()
kp1, des1 = detector.detectAndCompute(gray, None)
kp2, des2 = detector.detectAndCompute(gray2, None)

# 比較器作成
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# 画像への特徴点の書き込み
matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

# 出力画像作成 表示
h1, w1, c1 = img.shape[:3]
h2, w2, c2 = img2.shape[:3]
height = max([h1,h2])
width = w1 + w2
out = np.zeros((height, width, 3), np.uint8)

cv2.drawMatches(img, kp1, img2, kp2, matches[:50],out, flags=0)
cv2.imshow("name", out)
cv2.waitKey(0)
