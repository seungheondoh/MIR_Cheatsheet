import json
import os
import youtube_dl
import wget
import argparse
import multiprocessing
from functools import partial
from contextlib import contextmanager
import torch

parser = argparse.ArgumentParser(description='thumbnail/meta crawling')
parser.add_argument('-a_dir', type=str, default='../dataset/audio')

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

def _multi_crawl(url, audio_path):
    if "list" in url:
        pass
    else:
        try:
            audio_crawl(url, audio_path + ".")
        except:
            pass

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def main():
    args = parser.parse_args()
    urls_dir = "../dataset/meta"
    lang = ['en', 'ko', 'fr']
    keyword = ['spring',
                'lounge',
                'winter',
                'workout',
                'meditation',
                'gym',
                'autumn',
                'cafe',
                'afternoon',
                'office',
                'nature',
                'summer',
                'road_trip',
                'club',
                'party',
                'late_night',
                'morning']
    save_path = []
    url_list = []
    for tag in keyword:
        for la in lang:
            json_list = os.listdir(os.path.join(urls_dir, tag, la))
            for jfile in json_list:
                f_url = json.load(open(os.path.join(urls_dir, tag, la, jfile), 'r', encoding='utf-8'))['url']
                youtube_id = f_url.split("https://www.youtube.com/watch?v=")[-1]
                audio_path = os.path.join(args.a_dir, tag, la, youtube_id)
                if not os.path.exists(os.path.dirname(audio_path)):
                    os.makedirs(os.path.dirname(audio_path))
                save_path.append(audio_path)
                url_list.append(f_url)
                
    with poolcontext(processes = multiprocessing.cpu_count()-2) as pool:
        pool.starmap(_multi_crawl, zip(url_list, save_path))
    
if __name__ == '__main__':
    main()