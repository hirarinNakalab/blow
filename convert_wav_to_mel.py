import shutil
import os
import glob
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def get_meldb(filename):
    mel = np.load(filename)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    return mel_db

def save_fig():
    noised_path = "original"
    cleaned_path = "submit"

    for noised_file in sorted(glob.glob(noised_path+"/*.npy")):
        cleaned_file = noised_file.replace(noised_path, cleaned_path).replace("noised_", "")
        noised_mdb = get_meldb(noised_file)
        cleaned_mdb = get_meldb(cleaned_file)
        fig, axes = plt.subplots(2, 1)
        for ax, mdb, title in zip(axes, [noised_mdb, cleaned_mdb], ["noised", "cleaned"]):
            ax.imshow(mdb)
            ax.set_title(title)
        plt.savefig("./fig/{}.png".format(os.path.basename(noised_file).replace(".npy", "")))
        plt.close()

def calc_mse():
    noised_path = "original"
    cleaned_path = "submit"

    for noised_file in sorted(glob.glob(noised_path + "/*.npy")):
        cleaned_file = noised_file.replace(noised_path, cleaned_path).replace("noised_", "")
        noised_mel = np.load(noised_file)
        cleaned_mel = np.load(cleaned_file)
        score = mean_squared_error(noised_mel, cleaned_mel)
        print(f"{noised_file} => MSE: {score}")

def wav_to_mel():
    data_path = "./res/blow/audio"
    noised_path = "original"
    submit_path = "./submit"

    for noised_file in sorted(glob.glob(noised_path + "/*.npy")):
        fn = os.path.basename(noised_file).split('_')[2].replace(".npy", "")
        cleaned_fn = f"{data_path}/noised_{fn}_to_raw.wav"
        y, sr = librosa.load(cleaned_fn)
        mel = librosa.feature.melspectrogram(y)

        npy_fn = "_".join(["tgt", fn]) + ".npy"
        npy_fn = os.path.join(submit_path, npy_fn)
        np.save(file=npy_fn, arr=mel, allow_pickle=False, fix_imports=False)
        print(f"save {npy_fn}")

def save_to_zip():
    shutil.make_archive('submit-data', 'zip', '/home/owner/blow/submit')

def check_audio_length(visualize=False):
    cleaned_path = "./res/blow/audio"
    noised_path = "./wav_bck"

    for noised_file in sorted(glob.glob(noised_path + "/noised_*.wav")):
        cleaned_file = os.path.basename(noised_file).replace("tgt_", "").replace(".wav", "")
        cleaned_file = f"{cleaned_path}/{cleaned_file}_to_raw.wav"
        noised, sr = librosa.load(noised_file)
        t_size = len(noised)
        amp = np.max(np.abs(noised))
        cleaned, sr = librosa.load(cleaned_file)
        cleaned = cleaned[:t_size]*amp
        librosa.output.write_wav(cleaned_file, cleaned, sr=sr, norm=False)
        print(f"wrote {cleaned_file}")
        if visualize:
            fig, axes = plt.subplots(2, 1)
            for ax, wave in zip(axes, [noised, cleaned]):
                ax.plot(wave)
            plt.show()
            plt.close()

if __name__ == '__main__':
    check_audio_length(visualize=True)
    wav_to_mel()
    save_fig()
    calc_mse()
    save_to_zip()
