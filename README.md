# VAD Web App

Minimal Flask web UI for the existing RMS-based Voice Activity Detection (VAD).

Project structure

vad-web-app/
├── app.py                 # Flask application
├── vad.py                 # Existing VAD logic (process_audio, save_segments)
├── templates/
│   └── index.html         # Upload form + results
├── static/                # (optional) static assets
├── uploads/               # Uploaded files are saved here
├── output/                # Extracted speech clips are written here
├── data/                  # (optional) sample data
│   └── test_data/
└── requirements.txt

Quick start (Windows PowerShell)

1. Open a terminal and create / activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Run the app locally:

```powershell
python app.py
```

4. Open in your browser:

```
http://127.0.0.1:5000
```

Upload behavior

- Upload a single `.wav` or `.flac` file from the UI.
- On each new upload the app clears the `output/` folder and then processes the uploaded file.
- Detected speech segments (start, end in seconds) appear on the page.
- Extracted speech clips are saved to `output/` with names like `sample_<file>_segment_<n>.wav` and are available for download.

Notes about VAD integration

- The app uses `process_audio(file_path)` from `vad.py`. That function should return a list of `(start_time, end_time)` tuples in seconds.
- The app uses `save_segments(audio, sample_rate, segments, file_index)` to write audio clips to `output/`.
- Do NOT modify `vad.py` unless you intend to change the VAD behavior.

Making the app publicly accessible (quick options)

- Local tunnel (temporary): use `ngrok`:

```powershell
ngrok http 5000
```

- Free hosting (persistent): deploy to Railway, Render, or Replit. Ensure `app.py` uses the `PORT` env var and binds `0.0.0.0`.

Production notes

- For production, run under a WSGI server (e.g. `waitress` on Windows or `gunicorn` on Linux) instead of `python app.py`.

Contact

If you want, I can create a prepared `Procfile`, Dockerfile, or step-by-step Railway deployment instructions next.