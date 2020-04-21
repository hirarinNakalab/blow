from audiotsm import wsola
from audiotsm.io.array import ArrayReader, ArrayWriter

import os
import glob
import librosa
import numpy as np

def time_stretch(input_fn, output_fn, speed):
    data, sr = librosa.load(input_fn)
    data = data.reshape(1, -1)
    reader = ArrayReader(data)
    writer = ArrayWriter(channels=1)
    tsm = wsola(channels=1, speed=speed)
    tsm.run(reader, writer)
    output = np.ascontiguousarray(writer.data.T)
    output = output.flatten()
    librosa.output.write_wav(output_fn, output, sr=22050)


if __name__ == '__main__':
    base = './wav'
    search_path = f"{base}/*.wav"

    for file in glob.glob(search_path):
        for speed in [1.05, 0.95]:
            fn = os.path.basename(file).replace(".wav", "").split("_")
            pattern, num = '_'.join(fn[:-1]), fn[-1]
            output_fn = f"{base}/{pattern}_x{speed}-{num}.wav"
            time_stretch(file, output_fn, speed)