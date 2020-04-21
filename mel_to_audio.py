import glob
import os

import librosa
import numpy as np


if __name__ == '__main__':
    data_path = "./original"

    search_path = f"{data_path}/*.npy"
    for i, file in enumerate(glob.glob(search_path)):
        print(file)
        mel = np.load(file)
        audio = librosa.feature.inverse.mel_to_audio(mel)
        filename = os.path.basename(file).replace(".npy", "")
        wav_filepath = f"./wav/{filename}.wav"
        librosa.output.write_wav(wav_filepath, audio, sr=22050, norm=False)
        print(f"wrote wav to {wav_filepath}.")