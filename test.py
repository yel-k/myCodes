import pytesseract,cv2
import numpy as np
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image,ImageTk
enhance_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image0.jpg'

# Read the image
image = cv2.imread(enhance_path, 0)
rotated_image = cv2.rotate(image, cv2.ROTATE_180)
# # Invert the image
# inverted_image = cv2.bitwise_not(image)
# # Define a kernel
# kernel = np.ones((1, 1), np.uint8)

# # Erosion
# erosion = cv2.erode(inverted_image, kernel, iterations = 1)

# # Dilation
# dilation = cv2.dilate(erosion, kernel, iterations = 10)
# erote='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/erortetest.jpg'
# dilate='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/dilatetest.jpg'
# cv2.imwrite(erote,erosion)
# cv2.imwrite(dilate,dilation)
# image = cv2.bitwise_not(dilation)

img='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/imgtest.jpg'
cv2.imwrite(img,rotated_image)
# image = Image.open(enhance_path)
# # Perform OCR using PyTesseract
text = pytesseract.image_to_string(rotated_image,lang='eng')
print(text)