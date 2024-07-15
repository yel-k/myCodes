import os

rted_path='C:/Users/htike/OneDrive/Documents/Payment Confirmation System/images/enhanced_image_rt.jpg'

if os.path.exists(rted_path):
    os.remove(rted_path)
    print("File deleted successfully")
else:
    print("The file does not exist")
