import os

# Paths to image folders
folders = [
    './images/monitor1',
    './images/monitor2',
    './images/forgotten'
]

def clear_images():
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
        else:
            print(f"Folder does not exist: {folder}")

if __name__ == "__main__":
    clear_images()
