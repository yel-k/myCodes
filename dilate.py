import cv2
import numpy as np
img=cv2.imread("images/Screenshot (17).jpg",0)
kernel = np.zeros((3,3), np.uint8)
# Apply dilation
dilated = cv2.dilate(img, kernel, iterations=3)
thresh1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 2)
thresh2 = cv2.adaptiveThreshold(dilated, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 2)
cv2.imshow("img",img)
cv2.imshow("dilate",dilated)
cv2.imshow("img2",thresh1)
cv2.imshow("dilate2",thresh2)
cv2.waitKey(0)