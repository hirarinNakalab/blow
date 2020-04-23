import glob
import shutil
import os

if __name__ == '__main__':
    dirs = "wav_dat wav_bck dat fig original" \
           " res res/model res/audio submit".split()

    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)

    original_path = "./original"
    for file in glob.glob(f"dist-data/noised_tgt/*.npy"):
        fn = os.path.basename(file)
        shutil.copyfile(file, f"{original_path}/{fn}")