import glob
import os

import librosa
import numpy as np
import zipfile


if __name__ == '__main__':
    data_path = "./dist-data.zip"
    extract_path = data_path.replace(".zip", "")
    with zipfile.ZipFile(data_path) as zf:
        zf.extractall(extract_path)

    output_path = "./wav"
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for i, file in enumerate(glob.glob(f"{extract_path}/*/*.npy")):
        mel = np.load(file)
        audio = librosa.feature.inverse.mel_to_audio(mel)
        filename = os.path.basename(file).replace(".npy", "")
        wav_filepath = f"{output_path}/{filename}.wav"
        librosa.output.write_wav(wav_filepath, audio, sr=22050, norm=False)
        print(f"save converted wav to {wav_filepath}.")