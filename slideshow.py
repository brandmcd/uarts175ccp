import os
import tkinter as tk
from PIL import Image, ImageTk

def resize_image(img, max_width, max_height):
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
    screen_width = root.winfo_vrootwidth()
    screen_height = root.winfo_vrootheight()

    monitor_width = screen_width // 2
    x_offset = monitor_width  # Second monitor starts here
    y_offset = 0

    root.geometry(f"{monitor_width}x{screen_height}+{x_offset}+{y_offset}")
    label = tk.Label(root)
    label.pack()

    while True:
        images = [f for f in os.listdir(directory) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if images:
            for img_file in images:
                try:
                    img_path = os.path.join(directory, img_file)
                    img = Image.open(img_path)
                    img = resize_image(img, monitor_width, screen_height)
                    photo = ImageTk.PhotoImage(img)
                    label.config(image=photo)
                    label.image = photo
                    root.update_idletasks()
                    root.update()
                    print(f"Displaying: {img_file}")
                    root.after(5000)
                except Exception as e:
                    print(f"Error displaying {img_file}: {e}")
        else:
            print("No images to display.")
        root.after(30000)

if __name__ == "__main__":
    display_slideshow('./images/monitor2')