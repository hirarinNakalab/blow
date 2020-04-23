import argparse

from audiotsm import wsola
from audiotsm.io.array import ArrayReader, ArrayWriter

import os
import glob
import librosa
import numpy as np


def time_stretch(data, speed):
    data = data.reshape(1, -1)
    reader = ArrayReader(data)
    writer = ArrayWriter(channels=1)
    tsm = wsola(channels=1, speed=speed)
    tsm.run(reader, writer)
    output = np.ascontiguousarray(writer.data.T)
    output = output.flatten()
    return output

def pitch_shift(data, n_steps):
    return librosa.effects.pitch_shift(data, 22050, n_steps=n_steps)

# def frame_shift(data, n_shift, sr=22050):
#     n_frame_div = 5
#     frame_length = 5 # [ms]
#     shift_sample = int(sr * (frame_length/1000) / n_frame_div)
#     head = np.zeros(shift_sample*n_shift)
#     tail = np.zeros(shift_sample*(n_frame_div-n_shift))
#     data = np.concatenate([head, data, tail])
#     return data



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data augmentation script')
    parser.add_argument('--n_pitch_shift', default=3, type=int, required=True, help='(default=%(default)s)')
    parser.add_argument('--n_stretch', default=3, type=int, required=True, help='(default=%(default)s)')
    args = parser.parse_args()

    base = './wav'
    search_path = f"{base}_bck/*.wav"

    for file in glob.glob(search_path):
        fn = os.path.basename(file)
        fn = fn.replace(".wav", "").split("_")
        pattern, num = '_'.join(fn[:-1]), fn[-1]
        data, sr = librosa.load(file)

        for steps in np.linspace(-0.125, 0.130, args.n_pitch_shift, endpoint=False):
            pitched = pitch_shift(data, steps)
            p_shift = f"({steps:.3f})pit"
            if "noised" in file:
                for n in np.linspace(0.98, 1.01, args.n_stretch, endpoint=False):
                    stretched = time_stretch(pitched, n)
                    n_stretch = f"{n:.3f}strc"

                    output_fn = f"{base}/{pattern}_{p_shift}-{n_stretch}-{num}.wav"
                    librosa.output.write_wav(output_fn, stretched, sr=22050)
                    print(output_fn)
            else:
                output_fn = f"{base}/{pattern}_{p_shift}-{num}.wav"
                librosa.output.write_wav(output_fn, pitched, sr=22050)
                print(output_fn)