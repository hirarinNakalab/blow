# Blow: bannam challenge

## Installation

Suggested steps are:

1. Clone repository.
1. Mark following directories in Pycharm to import .py files (src/models, src/utils)
1. Create a virtualenv environment (you can use the `requirements.txt` file).
1. Put dist-data.zip to project root directory (for example `blow/dist-data.zip`)
1. You can run program using .run file in PyCharm

## Set up
```
$ pip install -r requirements.txt
$ python mel_to_audio.py
$ python create_dir.py
```

### Data Augmentation
```
$ python data_augmentation.py --n_pitch_shift 3 --n_stretch 3
```

### Preprocessing

To preprocess the audio files:
```
python src/preprocess.py --path_in ../wav/ --extension .wav --path_out ../dat/ --sr 22050
python src/misc/rename_dataset.py --dataset bannam --path ../../dat/
```

### Training

To train Blow:
```
python src/train.py --path_data ../dat --model blow --multigpu --nepochs 100 --base_fn_out ../res/blow --sr 22050
```

### Convert 

To synthesize all audio with a given learnt model:
```
python src/synthesize.py --base_fn_model ../res/blow/ --path_out ../res/blow/audio/ --convert --split train+valid --force_source_speaker noised --force_target_speaker raw
python src/synthesize.py --base_fn_model ../res/blow/ --path_out ../res/blow/audio/ --convert --split test --force_source_speaker noised --force_target_speaker raw
```

### Convert audio in melspectrogram format and save into zip file

After doing this, figure comparing melspectrogram before/after convert.
and MSE between those spectrogram.
At last, submit-data.zip will be saved.
```
python convert_wav_to_mel.py
```
