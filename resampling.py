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
        output_path = "./down_16k"
    elif args.method == "up":
        cmd = "sox {} -r 22050 {}"
        output_path = "./up_22.05k"
    else:
        sys.exit(1)

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for in_file in glob.glob(f"{args.path_in}/*.wav"):
        out_file = os.path.basename(in_file)
        out_file = f"{output_path}/{out_file}"
        cmd_list = cmd.format(in_file, out_file).split(" ")
        subprocess.call(cmd_list)
        print(f"{args.method}sampled {in_file} to {out_file}")