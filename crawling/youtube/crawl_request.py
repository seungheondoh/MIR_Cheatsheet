import os
import argparse
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import multiprocessing as mp


def crawling_fn(url, dst_path):
    DOWNLOAD_API = {
        'url': url,
        'headers': {
            'Content-Type': 'audio/mpeg'
        },
        'params': {
            'download': 'true',
        }
    }
    response = requests.get(DOWNLOAD_API['url'],
                                headers=DOWNLOAD_API['headers'],
                                params=DOWNLOAD_API['params'],
                                auth=HTTPBasicAuth('user', 'pass')) 
    with open(dst_path, "wb") as f:
        f.write(response.content)

def main(args):
    if args.epidemic:
        df_eq_all= pd.read_csv("./dataset/meta/Epidemic_all.csv", index_col=0)
        list_of_urls = list(df_eq_all['url'])
        dst_paths = [os.path.join(args.save_path, "mp3", "epidemic", str(i) + ".mp3") for i in df_eq_all['epidemic_id']]
        with mp.Pool(processes=mp.cpu_count() // 2) as pool:
            pool.starmap(crawling_fn, zip(list_of_urls, dst_paths))

    if args.audiostock:
        df_audiostock = pd.read_csv("./dataset/meta/audiostock_all.csv", index_col=0)
        list_of_urls = list(df_audiostock['url'])
        fname_as = [i.split("/")[-2] for i in df_audiostock['url']]
        dst_paths = [os.path.join(args.save_path, "mp3", "audiostock", str(i) + ".mp3") for i in fname_as]
        with mp.Pool(processes=mp.cpu_count() // 2) as pool:
            pool.starmap(crawling_fn, zip(list_of_urls, dst_paths))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", default="./dataset")
    parser.add_argument("--epidemic", default=False, action="store_true")
    parser.add_argument("--audiostock", default=True, action="store_true")
    parser.add_argument("--freesound", default=False, action="store_true")
    args = parser.parse_args()
    main(args)