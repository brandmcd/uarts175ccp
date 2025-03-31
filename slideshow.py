import os
import tkinter as tk
from PIL import Image, ImageTk

def resize_image(img, max_width, max_height):
    """Resize the image while maintaining aspect ratio."""
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height

    # Adjust to fit within max dimensions
    if img_width / max_width > img_height / max_height:
        # Fit to width
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        # Fit to height
        new_height = max_height
        new_width = int(max_height * aspect_ratio)

    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def display_slideshow(directory):
    root = tk.Tk()

    # Get all available screen dimensions using winfo_screen()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get virtual screen info to detect second monitor
    virtual_width = root.winfo_vrootwidth()
    virtual_height = root.winfo_vrootheight()

    # Determine if there is a second monitor
    if virtual_width > screen_width:
        # Place on the second monitor (x_offset moves it to the right)
        x_offset = screen_width
    else:
        # If no second monitor, place it on the primary screen
        x_offset = 0

    # Dynamically set window size to full screen
    root.geometry(f"{screen_width}x{screen_height}+{x_offset}+0")
    label = tk.Label(root)
    label.pack()

    while True:
        images = [f for f in os.listdir(directory) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if images:
            for img_file in images:
                img_path = os.path.join(directory, img_file)
                
                # Open and resize image
                img = Image.open(img_path)
                img = resize_image(img, screen_width, screen_height)
                
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo
                root.update_idletasks()
                root.update()
                print(f"Displaying: {img_file}")
                root.after(60000)  # 1-minute slideshow
        else:
            print("No images to display.")
        root.after(60000)

if __name__ == "__main__":
    display_slideshow('./images/monitor2')
