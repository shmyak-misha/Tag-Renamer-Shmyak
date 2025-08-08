import os
from mutagen.easyid3 import EasyID3
from tkinter import Tk, filedialog

# Hide the root window
root = Tk()
root.withdraw()

# Ask user to select a folder
selected_folder = filedialog.askdirectory(title="Select folder with MP3 files")
if not selected_folder:
    print("No folder selected.")
    exit()

for filename in os.listdir(selected_folder):
    if filename.lower().endswith(".mp3"):
        mp3_path = os.path.join(selected_folder, filename)
        try:
            audio = EasyID3(mp3_path)
        except Exception:
            from mutagen.id3 import ID3
            audiofile = ID3()
            audiofile.save(mp3_path)
            audio = EasyID3(mp3_path)
        audio['title'] = 'New Title'
        audio['artist'] = 'New Artist'
        audio.save()
        print(f"Updated: {mp3_path}")