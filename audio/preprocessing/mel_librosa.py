import os
import librosa
import random
import pickle
import numpy as np
import warnings

def query_mel_loader(audio_path):
    # Extract mel.
    fftsize = 1024
    window = 1024
    hop = 512
    melBin = 128
    sr = 22050
    y,_ = librosa.load(audio_path, sr=22050)
    S = librosa.core.stft(y, n_fft=fftsize, hop_length=hop, win_length=window)
    X = np.abs(S)

    mel_basis = librosa.filters.mel(sr, n_fft=fftsize, n_mels=melBin)
    mel_S = np.dot(mel_basis,X)

    # value log compression
    mel_S = np.log10(1+10*mel_S)
    mel_S = mel_S.astype(np.float32)

    mel_S = mel_S.T

    all_frames = mel_S.shape[0]
    num_frames = 129
    num_segment = int(all_frames/num_frames)
    
    mel_feat = np.zeros((num_segment, num_frames, 128))
    for seg_iter in range(num_segment):
        mel_feat[seg_iter] = mel_S[seg_iter*num_frames:(seg_iter+1)*num_frames,:]

    mel_feat -= 0.20
    mel_feat /= 0.25
    return mel_feat


def extractor(idx):
    fftsize = 1024
    window = 1024
    hop = 512
    melBin = 128
    sr = 22050
    idx = id_to_path[MSD_id_to_7D_id[idx]]
    load_path = os.path.join(MSD_PATH, idx)
    save_name = os.path.join(FEATURE_PATH, idx).replace(".mp3",".npy")

    if not os.path.exists(os.path.dirname(save_name)):
        os.makedirs(os.path.dirname(save_name))

    if not os.path.exists(os.path.dirname(clip_name)):
        os.makedirs(os.path.dirname(clip_name))

    if os.path.isfile(save_name) == 1:
        print(save_name + '_file_already_extracted!')
    else:
        audio = query_mel_loader(load_path)
        np.save(save_name,audio)
        print("Finish Sample: ",save_name) 

if __name__ == '__main__':
    id_to_path = pickle.load(open("../media/bach1/dataset/MSD_ZSL/music_dataset_split/MSD_split/7D_id_to_path.pkl",'rb'))
    MSD_id_to_7D_id = pickle.load(open("../media/bach1/dataset/MSD_ZSL/music_dataset_split/MSD_split/MSD_id_to_7D_id.pkl",'rb'))