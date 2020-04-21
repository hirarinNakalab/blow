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

def frame_shift(data, n_shift, sr=22050):
    n_frame_div = 5
    frame_length = 5 # [ms]
    shift_sample = sr * (frame_length/1000) / n_frame_div
    data = np.concatenate([np.zeros(shift_sample*n_shift), data])
    return data


if __name__ == '__main__':
    base = './wav'
    search_path = f"{base}/*.wav"

    for file in glob.glob(search_path):
        fn = os.path.basename(file).replace(".wav", "").split("_")
        pattern, num = '_'.join(fn[:-1]), fn[-1]
        data, sr = librosa.load(file)

        for speed in [1.05, 0.95]:
            aug_method = f"x{speed}"
            data = time_stretch(data, speed)

            if "noised" in file:
                for steps in [-4, -2, 2, 4]:
                    data = pitch_shift(data, steps)
                    aug_method += f"({steps})pitch"
                    # for i in range(1, 5):
                    #     data = frame_shift(data, i)
                    #     aug_method += f"-{i}shift"
                    output_fn = f"{base}/{pattern}_{aug_method}-{num}.wav"
                    librosa.output.write_wav(output_fn, data, sr=22050)

            output_fn = f"{base}/{pattern}_{aug_method}-{num}.wav"
            librosa.output.write_wav(output_fn, data, sr=22050)