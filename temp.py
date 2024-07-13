import cv2
import numpy as np

def biggest_contours(contours, num=5):
    # Sort contours based on the area in descending order and take the top 'num' contours
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:num]
    biggest_contours = []
    for contour in sorted_contours:
        area = cv2.contourArea(contour)
        print(f'Contour area: {area}')
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if len(approx) == 4:
                biggest_contours.append(approx)
    return biggest_contours

# Example usage:
img = cv2.imread('C:/Users/htike/OneDrive/Pictures/kpay3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 20, 15, 15)
edged = cv2.Canny(gray, 100, 150)
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(edged, kernel, iterations=1)
contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Get the 5 biggest contours
biggest = biggest_contours(contours)

# Draw the biggest contours
img_copy = img.copy()
for i, contour in enumerate(biggest):
    cv2.drawContours(img_copy, [contour], -1, (0, 255, 0), 3)


cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow('img',img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
