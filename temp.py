
from PIL import Image

# Open an image file
with Image.open("C:/Users/htike/OneDrive/Pictures/kpay3.jpg") as img:
    # Rotate the image by 45 degrees
    rotated_img = img.rotate(90)

    # Save the rotated image
    

# Display the original and rotated images
img.show()
rotated_img.show()
