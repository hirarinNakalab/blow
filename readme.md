# Blow: bannam challenge

## Installation

Suggested steps are:

1. Clone repository.
1. Create a virtualenv environment (you can use the `requirements.txt` file).
1. Put dist-data.zip to project root directory (for example `blow/dist-data.zip`)

## Set up
```
$ pip install -r requirements.txt
$ python extract_zip.py
$ python mel_to_audio.py
$ python resampling.py --method down
```

### Data Augmentation
```
$ python data_augmentation.py --n_pitch_shift 3 --n_stretch 3
```

### Preprocessing

To preprocess the audio files:
```
$ cd src
$ python preprocess.py --path_in ../wav_dat/ --extension .wav --path_out ../dat/ --sr 22050
$ python ./misc/rename_dataset.py --dataset bannam --path ../dat/
```

### Training

To train Blow:
```
$ cd src
$ python train.py --path_data ../dat/ --model blow --multigpu --nepochs 100 --base_fn_out ../res/model/blow --sr 22050
```

### Convert 

To synthesize all audio with a given learnt model:
```
$ bash convert.sh
```

### Convert audio in melspectrogram format and save into zip file

After doing this, figure comparing melspectrogram before/after convert.  
And MSE between those spectrogram is calculated. At last, submit-data.zip will be saved.
```
$ python resampling --method up
$ python convert_wav_to_mel.py
```
