import tkinter as tk
import numpy as np
import mysql.connector,re,pytesseract,openpyxl,cv2
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog,messagebox
from PIL import Image,ImageTk
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Function to clear all items from the Treeview
def performOCR(file_path):
    try:
        # Load the image
        image = cv2.imread(file_path,0)
        # Perform OCR using PyTesseract
        text = pytesseract.image_to_string(image,lang='eng+mya')
    except:
        pass
    # Regular expressions to extract the data
    date_time_pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})'
    transaction_no_pattern = r'(\d{20})'
    amount_pattern = r'-([0-9,]+\.\d{2}) Ks'
    # Extracting the data
    date_time_match = re.search(date_time_pattern, text)
    if date_time_match:
        date_time = date_time_match.group(1)
    else:
        date_time = None  # or handle the absence of a match appropriately
    transaction_no_match = re.search(transaction_no_pattern, text)
    if transaction_no_match:
        transaction_no = transaction_no_match.group(1)
    else:
        transaction_no = None  # or handle the absence of a match appropriately
    amount_match = re.search(amount_pattern, text)
    if amount_match:
        amount = amount_match.group(1)
    else:
        amount = None  # or handle the absence of a match appropriately
    return date_time,transaction_no,amount
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
def checkResult(transaction_no):
    #confirm from database
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='pay_check')
    mycursor=conn.cursor()
    sql='select * from seller where transaction_no=%s;'
    val=(transaction_no,)
    mycursor.execute(sql,val)
    # Fetch the results
    results = mycursor.fetchall()
    if results:
        return True
    else:
        return False
def rotateImage(transaction_no_arr,transaction_no_count):
    rted_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image_rt.jpg'
    image=cv2.imread('C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image.jpg')
    date_time,transaction_no,amount,is_found=None,None,None,False
    # Rotate 180 degrees
    rotated_image = cv2.rotate(image, cv2.ROTATE_180)
    cv2.imwrite(rted_path,rotated_image)
    date_time,transaction_no,amount=performOCR(rted_path)
    if transaction_no:
            transaction_no_arr.append(transaction_no)
            transaction_no_count+=1
            is_found=checkResult(transaction_no)
            if is_found:
                return date_time,[transaction_no],amount,is_found,transaction_no_count
    return date_time,transaction_no_arr,amount,is_found,transaction_no_count
def rotateWithAngle(image_path, angle,transaction_no_arr,transaction_no_count):
    rted_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/rt_with_degree.jpg'
    date_time,transaction_no,amount,is_found=None,None,None,False
    # Load the image
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    # Calculate the center of the image
    center = (w // 2, h // 2)
    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, M, (w, h))
    cv2.imwrite(rted_path,rotated_image)
    date_time,transaction_no,amount=performOCR(rted_path)
    if transaction_no:
            transaction_no_arr.append(transaction_no)
            transaction_no_count+=1
            is_found=checkResult(transaction_no)
            if is_found:
                return date_time,[transaction_no],amount,is_found,transaction_no_count
    return date_time,transaction_no_arr,amount,is_found,transaction_no_count
def getAngle(file_path):
    # Read the image
    img = cv2.imread(file_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    # Initialize variables to find the longest line
    max_length = 0
    longest_line = None
    # Iterate over detected lines
    for r_theta in lines:
        r, theta = r_theta[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * r
        y0 = b * r
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        # Calculate the length of the line segment
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Check if the current line is the longest
        if length > max_length:
            max_length = length
            longest_line = (x1, y1, x2, y2)
        # Draw the line on the image
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # If a longest line was found, calculate its angle
    if longest_line:
        x1, y1, x2, y2 = longest_line
        dx = x2 - x1
        dy = y2 - y1
        angle_radians = np.arctan2(dy, dx)
        angle_degrees = np.degrees(angle_radians)
        return angle_degrees
def enhanceImage(file_path,double_height):
    date_time,transaction_no_arr,amount,is_found,transaction_no_count=None,[],None,False,0
    img = cv2.imread(file_path)
    original_image=img.copy()
    # Image modification
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 20, 15, 15)
    edged = cv2.Canny(gray, 5, 15)
    canny_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/canny_image.jpg'
    cv2.imwrite(canny_path,edged)
    # Define a kernel (structuring element) for dilation
    kernel = np.ones((5, 5), np.uint8)
    # Apply dilation
    dilated = cv2.dilate(edged, kernel, iterations=1)
    dilate_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/dilate_image.jpg'
    cv2.imwrite(dilate_path,dilated)
    # Contour detection
    contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    fivebiggest=biggestContours(contours)
    if len(fivebiggest)==0:
        angle=getAngle(file_path)
        if angle:
            quad=90
            if angle<0:
                quad=-90
            for i in range(4):
                date_time,transaction_no,amount,is_found,transaction_no_count=rotateWithAngle(file_path,angle+(i*quad),transaction_no_arr,transaction_no_count)
                if is_found:
                    return date_time,[transaction_no],amount,is_found,transaction_no_count
    contourimg=img.copy()
    cv2.drawContours(contourimg, fivebiggest, -1, (0, 255, 0), 3)
    contour_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/contour_image.jpg'
    cv2.imwrite(contour_path,contourimg)
    for biggest in fivebiggest:
        # global k
        # Pixel values in the original image
        points = biggest.reshape(4, 2)
        input_points = np.zeros((4, 2), dtype="float32")
        points_sum = points.sum(axis=1)
        input_points[0] = points[np.argmin(points_sum)]
        input_points[3] = points[np.argmax(points_sum)]
        points_diff = np.diff(points, axis=1)
        input_points[1] = points[np.argmin(points_diff)]
        input_points[2] = points[np.argmax(points_diff)]
        (top_left, top_right, bottom_right, bottom_left) = input_points
        bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
        top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
        right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
        left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))
        # Output image size
        max_width = max(int(bottom_width), int(top_width))
        max_height = max(int(left_height), int(right_height))
        if double_height:
            max_width=400
            max_height=800
            # max_height=max_width*2
        else:
            max_width=800
            max_height=400
            # max_height=max_width//2
        # Desired points values in the output image
        converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
        # Perspective transformation
        matrix = cv2.getPerspectiveTransform(input_points, converted_points)
        img_output = cv2.warpPerspective(original_image, matrix, (max_width, max_height))
        enhance_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image.jpg'
        cv2.imwrite(enhance_path, img_output)
        # k+=1
        date_time,transaction_no,amount=performOCR(enhance_path)
        if transaction_no:
            transaction_no_arr.append(transaction_no)
            transaction_no_count+=1
            is_found=checkResult(transaction_no)
            if is_found:
                return date_time,[transaction_no],amount,is_found,transaction_no_count
        else:
            date_time,transaction_no,amount,is_found,transaction_no_count=rotateImage(transaction_no_arr,transaction_no_count)
            if is_found:
                return date_time,[transaction_no],amount,is_found,transaction_no_count
    return date_time,transaction_no_arr,amount,is_found,transaction_no_count
# k=0
def clearTreeview(tree):
    for item in tree.get_children():
        tree.delete(item)
def fetchData():
    clearTreeview(tree)
    #confirm from database
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='pay_check')
    mycursor=conn.cursor()
    sql='select * from seller;'
    mycursor.execute(sql)
    # Fetch the results
    results = mycursor.fetchall()
    for row in results:
        tree.insert("", "end", values=(row[0],row[1],row[2],row[3]))    
    conn.close()
def confirmPayment(transactionId):
    #confirm from database
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='pay_check')
    mycursor=conn.cursor()
    sql='select * from seller where transaction_no=%s;'
    val=(transactionId,)
    mycursor.execute(sql,val)
    # Fetch the results
    results = mycursor.fetchall()
    if results:
        for row in results:
            if row[3]:
                messagebox.showwarning("Information","Payment already confirmed!!!")
            else:
                messagebox.showinfo("Information", f"Payment Found!\nTransaction Date- {row[0]}\nTransaction Id- {row[1]}\nAmount- {row[2]}")
                updatesql='update seller set confirm=True where transaction_no=%s;'
                mycursor.execute(updatesql,val)
                conn.commit()
    else:
        messagebox.showinfo("Information", f"Payment not found in the records!")
    conn.close()
def storeFromExcel(file_path):
    # Define variable to load the dataframe
    dataframe = openpyxl.load_workbook(file_path)
    # Define variable to read sheet
    dataframe1 = dataframe.active
    # Iterate the loop to read the cell values
    temp=''
    for row in range(7, dataframe1.max_row-7):
        for col in dataframe1.iter_cols(1, dataframe1.max_column):
            temp+=str(col[row].value).strip()+"#"
        arr=temp.split("#")
        temp=''
        if not "0.00"==arr[3]:
            conn=mysql.connector.connect(host='localhost',user='root',password='root',database='pay_check')
            mycursor=conn.cursor()
            sql='insert ignore into seller(transaction_time,transaction_no,amount) values(%s,%s,%s);'
            val=(arr[0],arr[1],arr[3])
            mycursor.execute(sql,val)
            conn.commit()
            conn.close()
    messagebox.showinfo("Information","Record Updated!")
    fetchData()
def storeFromImage(file_path,isSeller=True):
    start_time=time.time()
    date_time,transaction_no,amount=None,None,None
    date_time,transaction_no,amount=performOCR(file_path)
    is_found=False
    count=0
    result_tran_arr=[None]
    if transaction_no:
        count+=1
    else:
        if not transaction_no:
            date_time,transaction_no_arr,amount,is_found,transaction_no_count=enhanceImage(file_path,True)
            count+=transaction_no_count
            for i in range(len(transaction_no_arr)):
                result_tran_arr.append(transaction_no_arr[i])
        if not is_found:
            date_time,transaction_no_arr,amount,is_found,transaction_no_count=enhanceImage(file_path,False)
            count+=transaction_no_count
            for i in range(len(transaction_no_arr)):
                result_tran_arr.append(transaction_no_arr[i])
        if count==0:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Total execution time: {execution_time} seconds")
            messagebox.showerror("Error","Image can't detect information!!!")
            return
        if count>0:
            transaction_no=result_tran_arr[len(result_tran_arr)-1]
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time} seconds")
    #store data to database
    if transaction_no:
        if isinstance(transaction_no, list):
            transaction_no=transaction_no[0]
        conn=mysql.connector.connect(host='localhost',user='root',password='root',database='pay_check')
        mycursor=conn.cursor()
        if isSeller:
            messagebox.showinfo("Information","Record Updated!")
            sql='insert ignore into seller(transaction_time,transaction_no,amount) values(%s,%s,%s);'
        else:
            sql='insert ignore into customer(transaction_time,transaction_no,amount) values(%s,%s,%s);'
        val=(date_time,transaction_no,amount)
        mycursor.execute(sql,val)
        conn.commit()
        conn.close()
        if not isSeller:
            confirmPayment(transaction_no)
    fetchData()
def storeData(file_path):
    if file_path:
        isExcel=".xlsx"==file_path[len(file_path)-5:]
        try:
            if(isExcel):
                storeFromExcel(file_path)
            else:
                storeFromImage(file_path)
        except Exception as e:
            # Handle errors in loading the image
            messagebox.showerror("Error", f"Failed to load image: {e}")
def clickSeller(event):
    # Open file dialog and select an image file
    file_path = filedialog.askopenfilename()
    storeData(file_path)
def dragAndDropSeller(event):
    file_path = event.data.strip('{').strip('}')
    storeData(file_path)
def clickCustomer(event):
    # Open file dialog and select an image file
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            storeFromImage(file_path,False)
        except Exception as e:
            # Handle errors in loading the image
            messagebox.showerror("Error", f"Failed to load image: {e}")
def dragAndDropCustomer(event):
    file_path = event.data.strip('{').strip('}')
    try:
        storeFromImage(file_path,False)   
    except Exception as e:
            # Handle errors in loading the image
            messagebox.showerror("Error", f"Failed to load image: {e}")
# remove images
# rted_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image_rt.jpg'
# enhance_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image.jpg'
# if os.path.exists(rted_path):
#     os.remove(rted_path)
# if os.path.exists(enhance_path):
#     os.remove(enhance_path)
root=TkinterDnD.Tk()  
root.title("Payment Confirmation System")
root.resizable(False,False)
root.geometry("830x600")
label=tk.Label(root,text="Income Records",font=('Ariel',14))
label.pack(fill='both' )
# Create and place the table (Treeview)
columns = ("transaction_time", "transaction_no", "amount", "confirm")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("transaction_time", text="Transaction Time")
tree.heading("transaction_no", text="Transaction No")
tree.heading("amount", text="Amount")
tree.heading("confirm", text="Confirm")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# button frame
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.X)
# Configure the columns to expand
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
labelseller=tk.Label(frame,text="Upload Recipient Data")
labelseller.grid(row=2, column=0, columnspan=1)
labelcustomer=tk.Label(frame,text="Upload Sender Data")
labelcustomer.grid(row=2, column=1, columnspan=1)
# Load the image using Pillow
image = Image.open('C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/drag-drop-upload.jpg')
image = image.resize((380, 210), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)
labeldd1=tk.Label(frame,image=photo)
labeldd1.grid(row=3, column=0, columnspan=1, pady=5)
labeldd2=tk.Label(frame,image=photo)
labeldd2.grid(row=3, column=1, columnspan=1, pady=5)
# Bind the click event to the label
labeldd1.bind("<Button-1>", clickSeller)
labeldd1.drop_target_register(DND_FILES)
labeldd1.dnd_bind('<<Drop>>',dragAndDropSeller)
labeldd2.bind("<Button-1>", clickCustomer)
labeldd2.drop_target_register(DND_FILES)
labeldd2.dnd_bind('<<Drop>>',dragAndDropCustomer)
fetchData()
# Run the application    
root.mainloop()