import os
import tkinter as tk
from PIL import Image, ImageTk

def display_images(directory):
    root = tk.Tk()
    label = tk.Label(root)
    label.pack()

    while True:
        #this will continuously check the directory for images and display them
        images = [f for f in os.listdir(directory) if f.endswith(('png', 'jpg', 'jpeg'))]
        if images:
            for img_file in images:
                # Loop through each image in the directory
                # Open and resize the image
                img_path = os.path.join(directory, img_file)
                img = Image.open(img_path)
                img = img.resize((800, 600), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                root.update_idletasks()
                root.update()
        else:
            print("No images to display.")
        # sleep for 5 seconds before checking for new images
        root.after(5000)

if __name__ == "__main__":
    display_images('./images/monitor1')
