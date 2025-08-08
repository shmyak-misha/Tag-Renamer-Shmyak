import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, render_template, request, redirect, url_for, flash
from mutagen.easyid3 import EasyID3
from werkzeug.utils import secure_filename
import shutil

#from mutagen.easyid3 import EasyID3
#EasyID3.RegisterTextKey('comment', 'COMM')
app = Flask(__name__)
app.secret_key = "secret"
UPLOAD_FOLDER = "uploads"
NEW_FOLDER = os.path.join(UPLOAD_FOLDER, "new")
os.makedirs(NEW_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        return render_template("index.html")
    title = request.form.get("title", "Tag")
    album = request.form.get("album", "")
    artist = request.form.get("artist", "")
    genre = request.form.get("genre", "")
    #comments = request.form.get("comments", "")
    files = request.files.getlist("mp3files")
    print("Files received:", [file.filename for file in files])
    if not files:
        flash("No files uploaded.")
        return redirect(url_for("index"))   
    for idx, file in enumerate(files, start=0):  # Start from 0
        rel_path = file.filename  # This preserves subfolders if present
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rel_path)
        new_path = os.path.join(NEW_FOLDER, rel_path)
        # Ensure parent directories exist
        upload_parent = os.path.dirname(upload_path)
        new_parent = os.path.dirname(new_path)
        if upload_parent and not os.path.exists(upload_parent):
            os.makedirs(upload_parent, exist_ok=True)
        if new_parent and not os.path.exists(new_parent):
            os.makedirs(new_parent, exist_ok=True)
        print("Saving:", upload_path)
        print("Absolute path:", os.path.abspath(upload_path))
        print("File size:", file.content_length)
        file.save(upload_path)
        print("Saved to:", upload_path)
        shutil.copy2(upload_path, new_path)
        try:
            audio = EasyID3(new_path)
        except Exception:
            from mutagen.id3 import ID3
            audiofile = ID3()
            audiofile.save(new_path)
            audio = EasyID3(new_path)
        title_formatted = f"{title}{idx+1:02d}"
        audio['title'] = title_formatted
        if artist:
            audio['artist'] = artist
        if album:
            audio['album'] = album
        if genre:
            audio['genre'] = genre
        #if comments:
        #    from mutagen.id3 import COMM
            #audio.tags.add(COMM(encoding=3, lang='eng', desc='', text=comments))
        audio.save()
    flash(f"Copied and updated {len(files)} MP3 files in 'new' folder with tag '{title} #'!")
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)