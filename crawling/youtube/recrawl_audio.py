import json
import os
import torch
import youtube_dl
import pandas as pd
import numpy as np
from pydub import AudioSegment
from pathlib import Path

def _get_audio(audio_path):
    audiobuffer = AudioSegment.from_file(audio_path, "mp3", start_second=0, duration=1)
    audio_numpy = np.frombuffer(audiobuffer.set_channels(1)._data, dtype=np.int16) / 32768
    return audio_numpy

def audio_crawl(url, audio_out_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'writeinfojson': False,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'outtmpl': audio_out_dir
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download = True)

def main():
    df_clean = pd.read_csv("D:/dataset/clean/df_clean.csv", index_col=0)
    errors = []
    for idx in range(len(df_clean)):
        print(idx)
        instance = df_clean.iloc[idx]
        _id = instance.name
        lang = instance['lang']
        tag = instance['tag']
        audio_root = 'D:\\dataset\\audio'
        audio_path = Path(audio_root, tag, lang, _id + ".mp3")
        try:
            _get_audio(audio_path)
        except:
            errors.append(_id)
    print(len(errors))
    # torch.save(errors, "./errors.pt")

if __name__ == '__main__':
    main()
    #df_clean = pd.read_csv("D:/dataset/clean/df_clean.csv", index_col=0)
    #err_list = torch.load("./errors.pt")
    #df_clean.drop(err_list).to_csv("D:/dataset/clean/df_clean.csv")