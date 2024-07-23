import numpy as np
import pytesseract,cv2
from matplotlib import pyplot as plt
def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def biggestContours(contours, num=5):
    # Sort contours based on the area in descending order and take the top 'num' contours
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:num]
    biggest_contours = []
    for contour in sorted_contours:
        area = cv2.contourArea(contour)
        if area > 50000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if len(approx) == 4:
                biggest_contours.append(approx)
    return biggest_contours
# Function to clear all items from the Treeview

# path='C:/Users/htike/OneDrive/Pictures/tt2.jpg'
# temp_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/temp.jpg'
# img=cv2.imread(path)
# rsimg=cv2.resize(img,(400,800))
# # cv2.imwrite(temp_path)

# original_image=img.copy()
# # Image modification
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = cv2.bilateralFilter(gray, 20, 15, 15)
# edged = cv2.Canny(gray, 5, 15)

# # Define a kernel (structuring element) for dilation
# kernel = np.ones((5, 5), np.uint8)
# # Apply dilation
# dilated = cv2.dilate(edged, kernel, iterations=1)
# cv2.imwrite(temp_path,dilated)

# #Contour detection
# contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# fivebiggest=biggestContours(contours)
# sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
# contourimg=img.copy()
# cv2.drawContours(contourimg, fivebiggest, -1, (0, 255, 0), 3)
# cv2.imwrite(temp_path,contourimg)
# for biggest in fivebiggest:
#     # Pixel values in the original image
#     points = biggest.reshape(4, 2)
#     input_points = np.zeros((4, 2), dtype="float32")
#     points_sum = points.sum(axis=1)
#     input_points[0] = points[np.argmin(points_sum)]
#     input_points[3] = points[np.argmax(points_sum)]
#     points_diff = np.diff(points, axis=1)
#     input_points[1] = points[np.argmin(points_diff)]
#     input_points[2] = points[np.argmax(points_diff)]
#     (top_left, top_right, bottom_right, bottom_left) = input_points
#     bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
#     top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
#     right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
#     left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
#     # Output image size
#     max_width = 800
#     max_height = 400
#     # Desired points values in the output image
#     converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
#     # Perspective transformation
#     matrix = cv2.getPerspectiveTransform(input_points, converted_points)
#     img_output = cv2.warpPerspective(original_image, matrix, (max_width, max_height))
#     text = pytesseract.image_to_string(img,lang='eng+mya')
#     print(text)
#     print("---------------------------------------------------------------------")
#     text = pytesseract.image_to_string(img_output,lang='eng+mya')
#     print(text)
#     cv2.imwrite(temp_path,img_output)
# display(path)
img=cv2.imread("images/enhanced_image_rt.jpg")
text = pytesseract.image_to_string(img,lang='eng+mya')
print(text)
cv2.waitKey(0)