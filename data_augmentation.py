from audiotsm import wsola
from audiotsm.io.array import ArrayReader, ArrayWriter

import os
import glob
import librosa
import numpy as np
import itertools

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

def frame_shift(data, n_shift, sr=22050):
    n_frame_div = 5
    frame_length = 5 # [ms]
    shift_sample = int(sr * (frame_length/1000) / n_frame_div)
    head = np.zeros(shift_sample*n_shift)
    tail = np.zeros(shift_sample*(n_frame_div-n_shift))
    data = np.concatenate([head, data, tail])
    return data


if __name__ == '__main__':
    base = './wav'
    search_path = f"{base}_bck/*.wav"

    for file in glob.glob(search_path):
        fn = os.path.basename(file).replace(".wav", "").split("_")
        pattern, num = '_'.join(fn[:-1]), fn[-1]
        data, sr = librosa.load(file)

        for steps in [0.125*x for x in [-2, -1, 1, 2]]:
            output = pitch_shift(data, steps)
            aug_method = f"({steps})pitch"
            if "noised" in file:
                for i in range(1, 4):
                    output = frame_shift(output, i)
                    aug_method += f"-{i}shift"
                    # for speed in [1.05, 0.95]:
                    #     aug_method += f-"x{speed}"
                    #     output = time_stretch(output, speed)
                    output_fn = f"{base}/{pattern}_{aug_method}-{num}.wav"
                    librosa.output.write_wav(output_fn, output, sr=22050)
                    print(output_fn)
            else:
                output_fn = f"{base}/{pattern}_{aug_method}-{num}.wav"
                librosa.output.write_wav(output_fn, output, sr=22050)
                print(output_fn)