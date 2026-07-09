import os
import argparse
import glob

import numpy as np
import librosa
import soundfile as sf
from datasets import load_dataset


SAMPLING_RATE = 16000
FRAME_DURATION_SEC = 0.02
HOP_DURATION_SEC = 0.01
FRAME_LENGTH = int(FRAME_DURATION_SEC * SAMPLING_RATE)
HOP_LENGTH = int(HOP_DURATION_SEC * SAMPLING_RATE)
THRESHOLD = 0.01
HANGOVER_FRAMES = 5


def preprocess_audio(audio, sr):
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    if sr != SAMPLING_RATE:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=SAMPLING_RATE)

    return audio.astype(np.float32)


def frame_audio(audio, frame_length, hop_length):
    frames = []
    for start in range(0, len(audio) - frame_length + 1, hop_length):
        frame = audio[start:start + frame_length]
        if len(frame) < frame_length:
            frame = np.pad(frame, (0, frame_length - len(frame)))
        frames.append(frame)
    return frames


def compute_rms_energy(frame):
    return float(np.sqrt(np.mean(np.square(frame))))


def classify_frames(frames, threshold, hangover_frames):
    labels = []
    hangover_counter = 0

    for frame in frames:
        energy = compute_rms_energy(frame)
        speech = 1 if energy > threshold else 0

        if speech == 1:
            labels.append(1)
            hangover_counter = hangover_frames
        elif hangover_counter > 0:
            labels.append(1)
            hangover_counter -= 1
        else:
            labels.append(0)

    return labels


def generate_segments(labels, hop_length, sample_rate):
    segments = []
    start_index = None

    for idx, label in enumerate(labels):
        if label == 1 and start_index is None:
            start_index = idx
        elif label == 0 and start_index is not None:
            segments.append((start_index * hop_length / sample_rate, idx * hop_length / sample_rate))
            start_index = None

    if start_index is not None:
        segments.append((start_index * hop_length / sample_rate, len(labels) * hop_length / sample_rate))

    return segments


def merge_segments(segments, max_gap=0.2):
    if not segments:
        return []

    merged = [segments[0]]
    for start, end in segments[1:]:
        prev_start, prev_end = merged[-1]
        gap = start - prev_end
        if gap < max_gap:
            merged[-1] = (prev_start, end)
        else:
            merged.append((start, end))
    return merged


def filter_segments(segments, min_duration=0.3):
    return [(start, end) for start, end in segments if (end - start) >= min_duration]


def save_segments(audio, sample_rate, segments, file_index):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    for seg_index, (start, end) in enumerate(segments):
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)
        segment_audio = audio[start_sample:end_sample]
        if segment_audio.size == 0:
            continue
        output_path = os.path.join(output_dir, f"sample_{file_index}_segment_{seg_index}.wav")
        sf.write(output_path, segment_audio, sample_rate)


def process_sample(sample):
    audio = sample["audio"]["array"]
    sr = sample["audio"]["sampling_rate"]

    audio = preprocess_audio(audio, sr)
    frames = frame_audio(audio, FRAME_LENGTH, HOP_LENGTH)
    labels = classify_frames(frames, THRESHOLD, HANGOVER_FRAMES)
    segments = generate_segments(labels, HOP_LENGTH, SAMPLING_RATE)
    return segments


def process_audio(file_path):
    audio, sr = librosa.load(file_path, sr=SAMPLING_RATE, mono=True)
    sample = {"audio": {"array": audio, "sampling_rate": sr}}
    raw_segments = process_sample(sample)
    merged = merge_segments(raw_segments, max_gap=0.2)
    filtered = filter_segments(merged, min_duration=0.3)
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Simple RMS-based VAD with dataset/local fallback")
    parser.add_argument("--local_dir", type=str, default=None, help="Path to folder with WAV files to use as fallback")
    args = parser.parse_args()

    # Try gated dataset first (only request first 3 samples to limit downloads)
    try:
        ds = load_dataset(
            "talkbank/callhome",
            "eng",
            split="train[:3]",
            token=os.environ.get("HF_TOKEN"),
        )
        print("Loaded talkbank/callhome (first 3 samples)")
        for i, sample in enumerate(ds):
            raw_segments = process_sample(sample)
            merged = merge_segments(raw_segments, max_gap=0.2)
            filtered = filter_segments(merged, min_duration=0.3)
            save_segments(sample["audio"]["array"], SAMPLING_RATE, filtered, i)
            print(f"Sample {i}: {filtered}")
        return
    except Exception as exc:
        print(f"Could not load talkbank/callhome: {exc}")

    # Try public Common Voice dataset
    try:
        print("Falling back to public dataset: common_voice (en)")
        ds = load_dataset("mozilla-foundation/common_voice", "en", split="train[:3]")
        for i, sample in enumerate(ds):
            raw_segments = process_sample(sample)
            merged = merge_segments(raw_segments, max_gap=0.2)
            filtered = filter_segments(merged, min_duration=0.3)
            save_segments(sample["audio"]["array"], SAMPLING_RATE, filtered, i)
            print(f"Sample {i}: {filtered}")
        return
    except Exception as exc2:
        print(f"Could not load fallback dataset: {exc2}")

    # Fallback to local WAV files
    if args.local_dir:
        local_dir = args.local_dir
    else:
        local_dir = "data/test_audio"

    if not os.path.isdir(local_dir):
        print(f"Local folder '{local_dir}' not found; skipping local-file fallback.")
        return

    audio_paths = sorted(
        glob.glob(os.path.join(local_dir, "**", "*.wav"), recursive=True)
        + glob.glob(os.path.join(local_dir, "**", "*.flac"), recursive=True)
    )
    if not audio_paths:
        print(f"No WAV or FLAC files found in '{local_dir}'.")
        return

    print(f"Processing {len(audio_paths)} local audio files from '{local_dir}'")
    for i, p in enumerate(audio_paths[:3]):
        audio, sr = librosa.load(p, sr=SAMPLING_RATE, mono=True)
        sample = {"audio": {"array": audio, "sampling_rate": sr}}
        raw_segments = process_sample(sample)
        merged = merge_segments(raw_segments, max_gap=0.2)
        filtered = filter_segments(merged, min_duration=0.3)
        save_segments(audio, SAMPLING_RATE, filtered, i)
        print(f"Local Sample {i} ({os.path.basename(p)}): {filtered}")


if __name__ == "__main__":
    main()
