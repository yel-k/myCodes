from PIL import Image,ImageTk
import mysql.connector,re,pytesseract,openpyxl,cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img=Image.open('C:/Users/htike/OneDrive/Pictures/kpay1.jpg')
rted_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/temp.jpg'
text = pytesseract.image_to_string(img,lang='eng')
rotated_img=img.rotate(3,expand=True)
text2 = pytesseract.image_to_string(rotated_img,lang='eng')
rotated_img.save(rted_path)
print(text)
print('---------------------------------------------')
print(text2)