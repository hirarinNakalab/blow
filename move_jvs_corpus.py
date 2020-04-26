import os
import re
import glob
import shutil
import argparse
import subprocess



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data transportation script')
    parser.add_argument('--path_out', default='', type=str, required=True, help='(default=%(default)s)')
    args = parser.parse_args()

    # search_path = "../japanese_speech_corpus/jvs_ver1/jvs*/parallel100/wav24kHz16bit/VOICEACTRESS100_*.wav"
    search_path = "./jvs_ver1/jvs*/parallel100/wav24kHz16bit/VOICEACTRESS100_*.wav"
    sp_pattern = r'jvs\d+'
    wav_pattern = r'VOICEACTRESS100_\d+.wav'

    for file in glob.glob(search_path):
        speaker = re.findall(sp_pattern, file)[0]
        fn = re.findall(wav_pattern, file)[0]
        fn = '_'.join([speaker, fn.split('_')[-1]])
        shutil.copyfile(file, f"./wav_dat/{fn}")

    if not os.path.exists(args.path_out):
        os.mkdir(args.path_out)

    for file in glob.glob(f"./wav_dat/*.wav"):
        fn = os.path.basename(file)
        out_file = f"{args.path_out}/{fn}"
        cmd = 'sox {} -r 22050 {}'.format(file, out_file)
        subprocess.call(cmd.split())