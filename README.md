# 🎙️ Voice Activity Detection (VAD) Web App

A minimal Flask-based web interface for an RMS-based Voice Activity Detection (VAD) system. This application allows users to upload audio files, detect speech segments, and download extracted speech clips.

---

## 📌 Overview

This project integrates a backend VAD pipeline with a simple web interface. It processes audio files to identify speech regions based on energy (RMS) thresholds and extracts those segments into separate `.wav` files.

---

## 🧱 Project Structure

```
vad-web-app/
├── app.py              # Flask application (routes + integration)
├── vad.py              # Core VAD logic (DO NOT MODIFY)
├── templates/
│   └── index.html      # UI: upload form + results display
├── static/             # Optional static assets (CSS, JS)
├── uploads/            # Stores uploaded audio files
├── output/             # Stores extracted speech segments
├── data/
│   └── test_data/      # Optional sample dataset
└── requirements.txt    # Dependencies
```

---

## ⚙️ How It Works

1. User uploads an audio file (`.wav` or `.flac`)
2. File is saved to `uploads/`
3. `process_audio(file_path)` detects speech segments
4. `save_segments(...)` extracts and saves segments to `output/`
5. UI displays:

   * Speech timestamps
   * Download links for extracted clips

---

## 🚀 Quick Start (Windows PowerShell)

### 1. Create & Activate Virtual Environment

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Run Application

```
python app.py
```

### 4. Open in Browser

```
http://127.0.0.1:5000
```

---

## 📤 Upload Behavior

* Accepts `.wav` and `.flac` files
* Clears `output/` before each new upload
* Displays detected segments:

  ```
  (0.55, 5.44)
  (6.10, 8.20)
  ```
* Saves clips as:

  ```
  sample_<file_index>_segment_<n>.wav
  ```
* Provides direct download links

---

## 🧠 VAD Integration Notes

* `process_audio(file_path)`

  * Returns: `[(start_time, end_time), ...]`
* `save_segments(audio, sample_rate, segments, file_index)`

  * Saves extracted audio clips

⚠️ Do NOT modify `vad.py` unless changing detection logic.

---

## 📸 Screenshots (Add These)

Add screenshots inside a `screenshots/` folder and reference them here:

### Upload Interface

```
![Upload UI](screenshots/upload.png)
```

### Results Display

```
![Results UI](screenshots/results.png)
```

👉 Tip: Capture:

* Before upload screen
* After processing results

---

## 🌐 Making It Public

### Option 1: Temporary (Local Tunnel)

```
ngrok http 5000
```

### Option 2: Free Hosting

* Railway
* Render
* Replit

Ensure:

```
app.run(host="0.0.0.0", port=PORT)
```

---

## 🏭 Production Notes

* Do NOT use Flask dev server in production
* Use:

  * `waitress` (Windows)
  * `gunicorn` (Linux)

Example:

```
pip install waitress
waitress-serve --listen=0.0.0.0:5000 app:app
```

---

## 🎯 Key Features

* Simple and clean web interface
* RMS-based speech detection
* Automatic audio segmentation
* Downloadable outputs
* Minimal and modular architecture

---

## ⚠️ Limitations

* Sensitive to background noise
* Fixed threshold-based detection
* Not optimized for real-time streaming

---

## 🔮 Future Improvements

* Replace RMS with WebRTC or ML-based VAD
* Add waveform visualization
* Real-time microphone input
* Improve noise robustness

---

## 📬 Contact

If you want help with:

* Deployment (Railway/Render)
* Docker setup
* UI improvements

Feel free to extend this project further.
