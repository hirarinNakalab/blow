import os
import zipfile


if __name__ == '__main__':
    data_path = "./dist-data.zip"
    extract_path = data_path.replace(".zip", "")
    with zipfile.ZipFile(data_path) as zf:
        zf.extractall(extract_path)

    dirs = "wav_dat wav_bck pt_dat fig" \
           " res res/model res/audio submit".split()

    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)