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

    # Get primary screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get virtual screen dimensions
    virtual_screen_width = root.winfo_vrootwidth()
    virtual_screen_height = root.winfo_vrootheight()

    print(f"Primary Screen: {screen_width}x{screen_height}")
    print(f"Virtual Screen: {virtual_screen_width}x{virtual_screen_height}")

    # Calculate Monitor 2's position and size
    if virtual_screen_width > screen_width:
        second_monitor_width = virtual_screen_width - screen_width
        x_offset = screen_width
        print(f"Detected Monitor 2 at: x={x_offset}, width={second_monitor_width}")
    else:
        print("No second monitor detected. Displaying on primary monitor.")
        second_monitor_width = screen_width
        x_offset = 0

    # Set the window size to match the second monitor and center it
    window_width = min(second_monitor_width, screen_width)
    window_height = screen_height
    centered_x = x_offset + (second_monitor_width - window_width) // 2
    centered_y = (screen_height - window_height) // 2

    print(f"Centering window on Monitor 2 at: {centered_x}, {centered_y}")
    root.geometry(f"{window_width}x{window_height}+{centered_x}+{centered_y}")

    label = tk.Label(root)
    label.pack()

    while True:
        images = [f for f in os.listdir(directory) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if images:
            for img_file in images:
                img_path = os.path.join(directory, img_file)
                img = Image.open(img_path)
                img = resize_image(img, window_width, window_height)

                photo = ImageTk.PhotoImage(img)
                label.config(image=photo)
                label.image = photo
                root.update_idletasks()
                root.update()
                print(f"Displaying: {img_file}")
                root.after(5000)  # Display each image for 5 seconds
        else:
            print("No images to display.")
        root.after(30000)

if __name__ == "__main__":
    display_slideshow('./images/monitor2')
