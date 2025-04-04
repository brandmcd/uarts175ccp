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

def display_images(directory):
    root = tk.Tk()
    virtual_width = root.winfo_vrootwidth()
    screen_height = root.winfo_vrootheight()

    monitor_width = virtual_width // 2
    x_offset = 0  # Left screen
    y_offset = 0

    root.geometry(f"{monitor_width}x{screen_height}+{x_offset}+{y_offset}")
    label = tk.Label(root)
    label.pack()

    last_photo = None

    while True:
        files = [f for f in os.listdir(directory) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if files:
            img_path = os.path.join(directory, files[0])
            try:
                img = Image.open(img_path)
                img = resize_image(img, monitor_width, screen_height)
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo
                last_photo = photo
                root.update_idletasks()
                root.update()
            except Exception as e:
                print(f"Failed to open image: {e}")
                if last_photo:
                    label.config(image=last_photo)
                    label.image = last_photo
        root.after(1000)

if __name__ == "__main__":
    display_images('./images/monitor1')
