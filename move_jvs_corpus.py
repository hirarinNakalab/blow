import os
import glob


if __name__ == '__main__':
    search_path = "../japanese_speech_corpus/jvs_ver1/jvs*/parallel100/wav24kHz16bit/VOICEACTRESS100_*.wav"
    for file in glob.glob(search_path):
        print(file)
