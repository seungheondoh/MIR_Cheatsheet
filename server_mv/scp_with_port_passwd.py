import os
import json
import torch
import pickle
from paramiko import SSHClient
from scp import SCPClient
import shutil

host = "#"
port = "#"
user = "#"
password = "#"

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname=host, 
            port = port,
            username=user,
            password=password)

# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())

mv_files = []
# list_of_dataset = ['deezer', 'openmic']
list_of_dataset = ['msd']
for dataset in list_of_dataset:
    scp.put(os.path.join(dataset, "annotation.pt") , f"/CML/dataset/{dataset}/annotation.pt")
    scp.put(os.path.join(dataset, "track_split.json") , f"/CML/dataset/{dataset}/track_split.json")
    track_split = json.load(open(os.path.join("." ,dataset, "track_split.json"), 'r'))
    for i in track_split['test_track']:
        if dataset == "msd":
            msd_to_id = pickle.load(open(os.path.join(dataset, "lastfm_annotation", "MSD_id_to_7D_id.pkl"), 'rb'))
            id_to_path = pickle.load(open(os.path.join(dataset, "lastfm_annotation", "7D_id_to_path.pkl"), 'rb'))
            fname = id_to_path[msd_to_id[i]].replace(".mp3",".npy")
        else:
            fname = str(i) + ".npy"
        source = os.path.join(dataset, "npy",fname) 
        target = f"/CML/dataset/{dataset}/npy/{fname}"
        scp.put(source, target)

jamendo_list = ["autotagging", "autotagging_top50tags", "autotagging_genre","autotagging_instrument", "autotagging_moodtheme"]
annotation = torch.load(os.path.join("jamendo", "annotation.pt"))
paths = []
for split in jamendo_list:
    scp.put(os.path.join("jamendo", f"{split}_track_split.json") , f"/CML/dataset/jamendo/{split}_track_split.json")
    track_split = json.load(open(os.path.join(".", "jamendo", f"{split}_track_split.json"), 'r'))
    paths.extend([annotation[i]["path"].replace(".mp3", ".npy") for i in track_split["test_track"]])

for fname in set(paths):
    source = os.path.join("jamendo","npy",fname) 
    target = os.path.join("/CML/dataset/jamendo/npy",fname)
    scp.put(source, target)
scp.close()
