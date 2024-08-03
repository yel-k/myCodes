import cv2
import matplotlib.pyplot as plt
import numpy as np
img1=cv2.imread("C:/Users/htike/OneDrive/Pictures/viberk.jpg",0)
img2=cv2.imread("C:/Users/htike/OneDrive/Pictures/kpay1.jpg",0)
orb=cv2.ORB_create()
kp1,des1=orb.detectAndCompute(img1,None)
kp2,des2=orb.detectAndCompute(img2,None)
imgkp1=cv2.drawKeypoints(img1,kp1,None)
imgkp2=cv2.drawKeypoints(img2,kp2,None)
bf=cv2.BFMatcher()
matches=bf.knnMatch(des1,des2,k=2)
good=[]
for m,n in matches:
    if m.distance<0.75*n.distance:
        good.append([m])
print(len(good))
img3=cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
# Create a resizable window
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Image2', cv2.WINDOW_NORMAL)
cv2.namedWindow('Image3', cv2.WINDOW_NORMAL)

# Display the image in the window
cv2.imshow('Image', imgkp1)
cv2.imshow('Image2', imgkp2)
cv2.imshow('Image3', img3)

cv2.waitKey(0)