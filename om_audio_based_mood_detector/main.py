import librosa
import numpy as np
import os
import matplotlib.pyplot as plt


def analyze_audio_file(filepath):
    print(f"Loading audio file: {filepath} ...")
    try:
        y, sr = librosa.load(filepath, sr=None)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        print("Please make sure the file is a .wav file and the path is correct.")
        return None

    print("Analyzing audio features...")

    # Extracting features
    tempo_array = librosa.feature.tempo(y=y, sr=sr)
    global_tempo = np.mean(tempo_array)

    rms = np.mean(librosa.feature.rms(y=y))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))

    return {
        "tempo": global_tempo,
        "energy": rms,
        "brightness": spectral_centroid,
        "zcr": zcr
    }


def visualize_features(features):
    """Plots a bar graph for the extracted audio features."""
    labels = ['Tempo (BPM)', 'Energy (RMS)', 'Brightness (Hz)', 'ZCR']
    values = [
        features['tempo'],
        features['energy'] * 100,       # scaled for visibility
        features['brightness'] / 1000,  # scaled for visibility
        features['zcr'] * 1000          # scaled for visibility
    ]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=['orange', 'green', 'blue', 'purple'])
    plt.title("Audio Feature Visualization")
    plt.ylabel("Scaled Values")
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Add value labels above each bar
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f"{bar.get_height():.2f}", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def get_mood_from_audio(features):
    tempo = features['tempo']
    energy = features['energy']
    brightness = features['brightness']
    zcr = features['zcr']

    print("\n" + "="*30)
    print("AUDIO FEATURE ANALYSIS")
    print("="*30)
    print(f"  - Tempo: {tempo:.0f} BPM")
    print(f"  - Energy (Loudness): {energy:.4f}")
    print(f"  - Brightness (Centroid): {brightness:.0f}")
    print(f"  - Noisiness (ZCR): {zcr:.4f}")

    mood = "Mixed / Chill"
    description = "A track with a mixed or neutral mood."

    if tempo > 125 and energy > 0.18 and brightness > 2000 and zcr > 0.08:
        mood = "Party / Workout"
        description = "A fast, loud, bright, and percussive track."
    elif tempo > 110 and energy > 0.15 and brightness > 1800 and zcr < 0.1:
        mood = "Happy / Upbeat"
        description = "An upbeat and bright song."
    elif energy > 0.2 and zcr > 0.1:
        mood = "Intense / Energetic"
        description = "A high-energy and 'noisy' track."
    elif tempo < 95 and energy < 0.1 and brightness < 1400:
        mood = "Sad / Melancholic"
        description = "A slow, quiet, and 'darker' track."
    elif tempo < 100 and energy < 0.12 and brightness < 1600 and zcr < 0.06:
        mood = "Calm / Studying"
        description = "A slow and mellow track."

    print("\n--- MOOD PREDICTION ---")
    print(f"Mood: {mood}")
    print(f"Context: {description}")
    print("="*30)

    # ✅ Call visualization after analysis
    visualize_features(features)


def main():
    while True:
        filepath = input("\nEnter the path to your .wav file (or 'q' to quit): ").strip().strip('"')
        if not filepath:
            continue
        if filepath.lower() == 'q':
            print("Goodbye!")
            break
        if not os.path.exists(filepath):
            print(f"File not found at: {filepath}")
            continue
        if not filepath.lower().endswith('.wav'):
            print("This script only supports .wav files.")
            continue

        features = analyze_audio_file(filepath)
        if features:
            get_mood_from_audio(features)


if __name__ == "__main__":
    main()
