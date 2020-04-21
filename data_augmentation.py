from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter

import os
import glob

def time_stretch(input_fn, output_fn, speed):
    with WavReader(input_fn) as reader:
        with WavWriter(output_fn, reader.channels, reader.samplerate) as writer:
            tsm = phasevocoder(reader.channels, speed=speed)
            tsm.run(reader, writer)

if __name__ == '__main__':
    base = './wav'
    search_path = f"{base}/*.wav"

    for file in glob.glob(search_path):
        for speed in [1.05, 0.95]:
            fn = os.path.basename(file).replace(".wav", "").split("_")
            pattern, num = '_'.join(fn[:-1]), fn[-1]
            output_fn = f"{base}/{pattern}_x{speed}-{num}.wav"
            time_stretch(file, output_fn, speed)