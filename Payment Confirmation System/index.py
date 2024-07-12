import tkinter as tk
import numpy as np
import mysql.connector,re,pytesseract,openpyxl,cv2
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog,messagebox
from PIL import Image,ImageTk
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Function to clear all items from the Treeview
def performOCR(file_path):
    # Load the image
    image = Image.open(file_path)
    # Perform OCR using PyTesseract
    text = pytesseract.image_to_string(image,lang='eng+mya')
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
def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest
def enhanceImage(file_path):
    img = cv2.imread(file_path)
    original_image=img.copy()
    # Image modification
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 20, 15, 15)
    edged = cv2.Canny(gray, 100, 150)
    # Define a kernel (structuring element) for dilation
    kernel = np.ones((5, 5), np.uint8)
    # Apply dilation
    dilated = cv2.dilate(edged, kernel, iterations=1)
    # Contour detection
    contours, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    biggest=biggest_contour(contours)
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
    # max_height = max(int(right_height), int(left_height))
    max_height = max(int(left_height), int(right_height))
    # Desired points values in the output image
    converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])
    # Perspective transformation
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(original_image, matrix, (max_width, max_height))
    cv2.imwrite('C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image.jpg', img_output)
    return 'C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image.jpg'
def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)
def fetch_data():
    clear_treeview(tree)
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
                messagebox.showinfo("Information", f"Payment Found! The amount is {row[2]}")
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
    fetch_data()
def storeFromImage(file_path,isSeller=True):
    date_time,transaction_no,amount=performOCR(file_path)
    if not transaction_no:
        enhanced_path=enhanceImage(file_path)
        date_time,transaction_no,amount=performOCR(enhanced_path)
    if not transaction_no:
        messagebox.showerror("Error","Image can't detect information!!!")
        exit
    #store data to database
    if transaction_no:
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
    fetch_data()
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
labelseller=tk.Label(frame,text="Upload Seller Data")
labelseller.grid(row=2, column=0, columnspan=1)
labelcustomer=tk.Label(frame,text="Upload Customer Data")
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
fetch_data()
# Run the application
root.mainloop()