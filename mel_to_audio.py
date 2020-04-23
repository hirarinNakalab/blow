import glob
import os
import librosa
import numpy as np
import shutil


if __name__ == '__main__':
    output_path = "./wav_dat"
    bck_path = "./wav_bck"
    extract_path = "./dist-data"

    for i, file in enumerate(glob.glob(f"{extract_path}/*/*.npy")):
        mel = np.load(file)
        audio = librosa.feature.inverse.mel_to_audio(mel)
        filename = os.path.basename(file).replace(".npy", "")
        wav_filepath = f"{output_path}/{filename}.wav"
        librosa.output.write_wav(wav_filepath, audio, sr=22050, norm=False)
        print(f"save converted wav to {wav_filepath}.")

    for file in glob.glob(f"{output_path}/*.wav"):
        fn = os.path.basename(file)
        shutil.copyfile(file, f"{bck_path}/{fn}")