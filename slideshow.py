import os
import tkinter as tk
from PIL import Image, ImageTk

def resize_image(img, max_width, max_height):
    """Resize the image while maintaining aspect ratio."""
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height

    if img_width / max_width > img_height / max_height:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(max_height * aspect_ratio)

    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def display_slideshow(directory):
    root = tk.Tk()

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Check for a second monitor using xrandr dimensions
    virtual_screen_width = root.winfo_vrootwidth()
    if virtual_screen_width > screen_width:
        x_offset = screen_width
    else:
        x_offset = 0

    # Position the window on the second monitor if detected
    root.geometry(f"{screen_width}x{screen_height}+{x_offset}+0")

    label = tk.Label(root)
    label.pack()

    while True:
        images = [f for f in os.listdir(directory)]
        if images:
            for img_file in images:
                img_path = os.path.join(directory, img_file)
                img = Image.open(img_path)
                img = resize_image(img, screen_width, screen_height)
                
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo
                root.update_idletasks()
                root.update()
                print(f"Displaying: {img_file}")
                #wait for 5 seconds before showing the next image
                root.after(5000) 
        else:
            print("No images to display.")
        root.after(30000)

if __name__ == "__main__":
    display_slideshow('./images/monitor2')
