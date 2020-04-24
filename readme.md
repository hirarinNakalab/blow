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
$ python resampling.py --method down --path_in wav_dat # downsampling to 16kHz
```

### Data Augmentation
```
$ python data_augmentation.py --path_in down_16k --sr 16000 --n_pitch_shift 3
```

### Preprocessing

To preprocess the audio files:
```
$ cd src
$ python preprocess.py --path_in ../down_16k/ --extension .wav --path_out ../pt_dat/ --sr 16000
$ python python rename_dataset.py --dataset bannam --path ../pt_dat/
```

### Training

To train Blow:
```
$ cd src
$ python train.py --path_data ../pt_dat/ --model blow --multigpu --nepochs 100 --base_fn_out ../res/model/blow --sr 16000
```

### Convert 

To synthesize all audio with a given learnt model:
```
$ cd src
$ bash convert.sh
```

### Convert audio to melspectrogram and save as zip file

After doing this, figures comparing melspectrogram before/after convert will be saved.  
And MSE between those spectrogram is calculated. At last, `./submit-data.zip` will be saved.
```
$ python resampling.py --method up --path_in res/audio/
$ python convert_wav_to_mel.py --path_in up_22.05k --path_compare wav_dat --path_npy dist-data/noiset_tgt/
```

### Clear Project files

You can initialize project do following.
```
$ bash clear_project.sh
```
