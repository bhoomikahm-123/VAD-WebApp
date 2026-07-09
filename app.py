import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from vad import process_audio, save_segments
import librosa

ALLOWED_EXTENSIONS = {"wav", "flac"}
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html", segments=None, output_files=None)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Clear previous output files before processing a new upload.
    for output_file in os.listdir(app.config["OUTPUT_FOLDER"]):
        output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_file)
        if os.path.isfile(output_path):
            os.remove(output_path)

    segments = process_audio(file_path)

    try:
        audio, sr = librosa.load(file_path, sr=16000, mono=True)
        file_index = os.path.splitext(filename)[0]
        save_segments(audio, sr, segments, file_index)
    except Exception:
        pass

    output_files = [f for f in os.listdir(app.config["OUTPUT_FOLDER"]) if os.path.isfile(os.path.join(app.config["OUTPUT_FOLDER"], f))]

    return render_template("index.html", segments=segments, output_files=output_files)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
