import argparse
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

def melspec(cleaned_file, noised_file):
    noised_mdb = get_meldb(noised_file)
    cleaned_mdb = get_meldb(cleaned_file)
    fig, axes = plt.subplots(2, 1)
    for ax, mdb, title in zip(axes, [noised_mdb, cleaned_mdb], ["noised", "cleaned"]):
        ax.imshow(mdb)
        ax.set_title(title)
    plt.savefig("./fig/{}.png".format(os.path.basename(noised_file).replace(".npy", "")))
    plt.close()

def mse(cleaned_file, noised_file):
    noised_mel = np.load(noised_file)
    cleaned_mel = np.load(cleaned_file)
    score = mean_squared_error(noised_mel, cleaned_mel)
    print(f"{noised_file} => MSE: {score}")

def fix_audio_length(path_in, path_compare, visualize=False):
    for noised_file in sorted(glob.glob(path_compare + "/noised_*.wav")):
        cleaned_file = os.path.basename(noised_file)
        cleaned_file = cleaned_file.replace("tgt_", "").replace(".wav", "")
        cleaned_file = f"{path_in}/{cleaned_file}_to_raw.wav"
        noised, sr = librosa.load(noised_file)
        t_size = len(noised)
        amp = np.max(np.abs(noised))
        cleaned, sr = librosa.load(cleaned_file)
        cleaned = cleaned[:t_size] * amp
        librosa.output.write_wav(cleaned_file, cleaned, sr=sr, norm=False)
        print(f"wrote {cleaned_file}")
        if visualize:
            fig, axes = plt.subplots(2, 1)
            for ax, wave in zip(axes, [noised, cleaned]):
                ax.plot(wave)
            plt.show()
            plt.close()

def wav_to_mel(path_in, path_npy):
    for noised_file in sorted(glob.glob(path_npy + "/*.npy")):
        fn = os.path.basename(noised_file).split('_')[2].replace(".npy", "")
        cleaned_fn = f"{path_in}/noised_{fn}_to_raw.wav"
        y, sr = librosa.load(cleaned_fn)
        mel = librosa.feature.melspectrogram(y)

        npy_fn = "_".join(["tgt", fn]) + ".npy"
        npy_fn = os.path.join("submit", npy_fn)
        np.save(file=npy_fn, arr=mel, allow_pickle=False, fix_imports=False)
        print(f"save {npy_fn}")

def save_to_zip():
    shutil.make_archive('submit-data', 'zip', './submit')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocessing script')
    parser.add_argument('--visualize', action='store_true')
    parser.add_argument('--path_in', default='', type=str, required=True, help='(default=%(default)s)')
    parser.add_argument('--path_compare', default='', type=str, required=True, help='(default=%(default)s)')
    parser.add_argument('--path_npy', default='', type=str, required=True, help='(default=%(default)s)')
    args = parser.parse_args()

    fix_audio_length(args.path_in, args.path_compare, args.visualize)
    wav_to_mel(args.path_in, args.path_npy)

    for noised_file in sorted(glob.glob(args.path_npy + "/*.npy")):
        fn = os.path.basename(noised_file).replace("noised_", "")
        cleaned_file = f"submit/{fn}"
        mse(cleaned_file, noised_file)
        melspec(cleaned_file, noised_file)

    save_to_zip()
