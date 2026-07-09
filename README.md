# 🎙️ VAD Web App

A minimal Flask-based web application for **Voice Activity Detection (VAD)** using RMS energy.

Users can upload an audio file and the app will:
- Detect speech segments
- Display timestamps
- Extract and save audio clips

---

## 🚀 Features

- Upload `.wav` or `.flac` audio files
- Detect speech segments (start & end time)
- Automatically extract speech clips
- Download processed audio segments
- Simple and clean UI

---

## 📁 Project Structure


```
vad-web-app/
├── app.py                # Flask application
├── vad.py                # VAD logic (process_audio, save_segments)
├── templates/
│   └── index.html        # Frontend UI
├── static/               # Static assets (optional)
├── uploads/              # Uploaded audio files
├── output/               # Extracted speech segments
├── data/                 # Sample data (optional)
│   └── test_data/
├── requirements.txt
├── Procfile              # For deployment
└── runtime.txt           # Python version (optional)

```

---

## ⚙️ Setup & Run Locally

### 1. Create virtual environment (recommended)

```bash
python -m venv .venv

Activate:

Windows

.\.venv\Scripts\activate

Mac/Linux

source .venv/bin/activate
```

```bash
2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
```bash
3. Run the app
python app.py
```
```bash
4. Open in browser
http://127.0.0.1:5000
```
📤 Upload Behavior
Upload a .wav or .flac file
Output folder is cleared on each upload
Speech segments are detected and displayed
Extracted clips saved as:
sample_<filename>_segment_<n>.wav

🧠 VAD Integration

The app uses functions from vad.py:
process_audio(file_path)

Returns:
[(start_time, end_time), ...]
save_segments(audio, sample_rate, segments, file_index)

🌐 Deployment (Render)

Deploy easily on Render:

👉 https://render.com

Settings:

Build Command

pip install -r requirements.txt

Start Command

gunicorn app:app
Required Files

Procfile

web: gunicorn app:app

runtime.txt (optional)

python-3.10.13
⚠️ Notes
Free tier sleeps after inactivity (~15 min)
First request may take ~30–60 seconds (cold start)
Avoid heavy dependencies for free deployment
🔧 Optional: Temporary Public URL

Use ngrok:

ngrok http 5000
📦 Tech Stack
Python
Flask
NumPy
Audio Processing (RMS-based VAD)
📌 Future Improvements
Real-time audio detection
Waveform visualization
AI-based speech classification
Upload multiple files
👩‍💻 Author

Bhoomika HM

⭐ If you like this project

Give it a ⭐ on GitHub and share!


---

