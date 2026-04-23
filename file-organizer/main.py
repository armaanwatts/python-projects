import os
import shutil

print("=== File Organizer Tool ===")

folder_path = input("Enter the folder path to organize: ")

if not os.path.exists(folder_path):
    print("❌ Folder not found!")
    exit()

files = os.listdir(folder_path)

extensions_map = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Music": [".mp3", ".wav"],
    "Programs": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css"],
    "Archives": [".zip", ".rar", ".7z"]
}

def get_folder_name(file_extension):
    for folder, extensions in extensions_map.items():
        if file_extension in extensions:
            return folder
    return "Others"

moved_count = 0

for file in files:
    file_path = os.path.join(folder_path, file)

    if os.path.isfile(file_path):
        ext = os.path.splitext(file)[1].lower()
        folder_name = get_folder_name(ext)

        target_folder = os.path.join(folder_path, folder_name)

        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        shutil.move(file_path, os.path.join(target_folder, file))
        moved_count += 1

print(f"\n✅ Done! Organized {moved_count} files successfully.")
