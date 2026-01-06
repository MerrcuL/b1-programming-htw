import os
import time

def main():
    folder_name = "lab_files"
    files = ["file1.txt", "file2.txt", "file3.txt"]
    new_name = "renamed_file.txt"

    print(f"Current Working Directory: {os.getcwd()}")

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")

    for filename in files:
        filepath = os.path.join(folder_name, filename)
        with open(filepath, 'w') as f:
            pass
    print(f"Created three files: {files}")

    print(f"Contents of '{folder_name}': {os.listdir(folder_name)}")

    old_path = os.path.join(folder_name, files[0])
    new_path = os.path.join(folder_name, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed '{files[0]}' to '{new_name}'.")

    print("Starting cleanup...")
    
    current_files = os.listdir(folder_name)
    for f in current_files:
        path = os.path.join(folder_name, f)
        os.remove(path)
        print(f"Deleted file: {f}")

    os.rmdir(folder_name)
    print(f"Folder '{folder_name}' removed. Cleanup complete.")

if __name__ == "__main__":
    main()