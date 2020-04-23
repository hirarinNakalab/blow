import subprocess
import argparse
import os
import sys
import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wav file resampling using sox (runs over preprocessed files)')
    parser.add_argument('--method', default='', type=str, required=True, help='(default=%(default)s)')
    parser.add_argument('--path_in', default='', type=str, required=True, help='(default=%(default)s)')
    args = parser.parse_args()

    if args.method == "down":
        cmd = "sox {} -r 16000 {}"
    elif args.method == "up":
        cmd = "sox {} -r 22050 {}"
    else:
        sys.exit(1)

    for file in glob.glob(f"{args.path_in}/*.wav"):
        cmd = cmd.format(file, file).split(" ")
        subprocess.call(cmd)
        print(f"{args.method}sampled {file}")