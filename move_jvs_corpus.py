import os
import re
import glob
import shutil
import subprocess



if __name__ == '__main__':
    search_path = "../japanese_speech_corpus/jvs_ver1/jvs*/parallel100/wav24kHz16bit/VOICEACTRESS100_*.wav"
    sp_pattern = r'jvs\d+'
    wav_pattern = r'VOICEACTRESS100_\d+.wav'

    for file in glob.glob(search_path):
        speaker = re.findall(sp_pattern, file)[0]
        fn = re.findall(wav_pattern, file)[0]
        fn = '_'.join([speaker, fn.split('_')[-1]])
        shutil.copyfile(file, )
        # "mkdir ../22.05k"
        # "find . -name "*.wav" -exec sox {} -r 22050 ../22.05k/{} \;"
