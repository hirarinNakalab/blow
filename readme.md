# Blow: bannam challenge

## Installation

Suggested steps are:

1. Clone repository on your home directory (for example `/home/your_name/blow`).
1. Create a virtualenv environment (you can use the `requirements.txt` file).
1. Put dist-data.zip to project root directory (for example `/home/your_name/blow/dist-data.zip`)

## Set up
```
$ pip install -r requirements.txt
$ python extract_zip.py
$ python mel_to_audio.py
```  
if you use JVS Corpus, please download file from [this link](https://drive.google.com/open?id=19oAw8wWn3Y7z6CKChRdAyGOB9yupL_Xt).  
Unzip file and put data on your home directory (for example `/home/your_name/jvs_ver1`).  
After that, do following.
```
$ python move_jvs_corpus.py --path_out 22.05k
```
if not, you must do following.
```
$ mkdir 22.05k
$ mv wav_dat/*.wav 22.05k/
```

### Data Augmentation
```
$ python data_augmentation.py --path_in 22.05k --sr 22050 --n_pitch_shift 3
```

### Preprocessing

To preprocess the audio files:
```
$ cd src
$ python preprocess.py --path_in ../22.05k/ --extension .wav --path_out ../pt_dat/ --sr 22050
$ python rename_dataset.py --dataset bannam --path ../pt_dat/
```

### Training

To train Blow:
```
$ cd src
$ python train.py --path_data ../pt_dat/ --model blow --multigpu --nepochs 100 --base_fn_out ../res/model/blow --sr 22050
```

### Convert 

To synthesize all audio with a given learnt model:
```
$ cd src
$ bash convert.sh
```

### Convert audio to melspectrogram and save as zip file

After doing this, figures comparing melspectrogram before/after convert will be saved.  
And MSE between those spectrogram is calculated. Finally, `./submit-data.zip` will be saved.  
```
$ python convert_wav_to_mel.py --path_in res/audio/ --path_compare wav_bck --path_npy dist-data/noised_tgt/
```

### Clear Project files

You can initialize project do following.
```
$ bash clear_project.sh
```
