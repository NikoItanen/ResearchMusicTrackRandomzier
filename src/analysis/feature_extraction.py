import librosa
import numpy as np

def extract_features(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None, duration=30)

    # Calculate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # Librosa return tempo as an array, so we take the first element out of it
    if hasattr(tempo, "__len__"):
        tempo = tempo[0]
    else:
        tempo = float(tempo)

    # Calculate spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = float(np.mean(spectral_centroid))

    # Calculate RMSE
    rmse = librosa.feature.rms(y=y)
    rmse_mean = float(np.mean(rmse))

    # Calculate spectral rolloff
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_rolloff_mean = float(np.mean(spectral_rolloff))

    return {
        "tempo": float(tempo),
        "centroid_mean": spectral_centroid_mean,
        "rmse_mean": rmse_mean,
        "spectral_rolloff_mean": spectral_rolloff_mean
    }

# Example usage
if __name__ == "__main__":
    file_path = "assets/audio/fma_medium/000/000002.mp3"
    features = extract_features(file_path)
    print(features)