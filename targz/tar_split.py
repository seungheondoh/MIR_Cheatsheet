import datetime as dt
import multiprocessing as mp
import os
import tarfile
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import argparse


def compress(targz_name, file_paths):
    tar = tarfile.open(targz_name, "w:gz")
    for name in file_paths:
        tar.add(name)
    tar.close()


def main(args):
    record_dir = os.path.join(args.save_path, "targz")
    os.makedirs(record_dir, exist_ok=True)
    dataset = [i.replace(".mp4", "") for i in os.listdir(os.path.join(args.save_path, "mp4")) if ".mp4" in i]
    items_per_file = 512
    num_items = len(dataset)
    num_records = int(np.ceil(num_items / items_per_file))
    file_splits = defaultdict(list)
    print(num_items) # 17452
    print(num_records)

    for item_idx in range(num_items):
        record_idx = item_idx % num_records
        file_splits[record_idx].append(item_idx)

    for record_idx, item_idxs in file_splits.items():
        r_path = os.path.join(record_dir, f'{record_idx}.tar.gz')
        file_paths = [os.path.join(args.save_path, "mp4", dataset[i]+".mp4") for i in item_idxs]
        compress(targz_name=r_path, file_paths=file_paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iter_download", default=False, type=bool)
    parser.add_argument("--save_path", default="./dataset/ml-20m/content")
    args = parser.parse_args()
    main(args)
