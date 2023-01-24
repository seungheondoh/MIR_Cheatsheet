import datetime as dt
import multiprocessing as mp
import os
import tarfile
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--save_path", default="./mp3/unbalanced_train")
parser.add_argument("--record_dir", default="./mp3/targz")
args = parser.parse_args()


def mp_fn(record_idx, item_idxs):
    r_path = os.path.join(args.record_dir, f'{record_idx}.tar.gz')
    dataset = [i for i in os.listdir(args.save_path)]
    file_paths = [os.path.join(args.save_path, dataset[i]) for i in item_idxs]
    compress(targz_name=r_path, file_paths=file_paths)

def compress(targz_name, file_paths):
    tar = tarfile.open(targz_name, "w:gz")
    for name in file_paths:
        tar.add(name)
    tar.close()


def main(args):
    os.makedirs(args.record_dir, exist_ok=True)
    dataset = [i for i in os.listdir(args.save_path)]
    items_per_file = 8192
    num_items = len(dataset)
    num_records = int(np.ceil(num_items / items_per_file))
    file_splits = defaultdict(list)
    print(num_items) # 17452
    print(num_records)

    for item_idx in range(num_items):
        record_idx = item_idx % num_records
        file_splits[record_idx].append(item_idx)

    with mp.Pool(processes=mp.cpu_count() - 5) as pool:
        pool.starmap(mp_fn, file_splits.items())        

if __name__ == "__main__":
    main(args)