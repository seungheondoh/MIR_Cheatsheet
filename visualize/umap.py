import os
import pandas as pd
import numpy as np
import json
import torch
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
import umap

idx_i = 1126
idx_j = 32119
idx_k = 406409

def _get_tag_artist_track_audio_xy(jointemb):
    vocab = list(jointemb.keys())
    x = [jointemb[i]['x'] for i in vocab]
    y = [jointemb[i]['y'] for i in vocab]

    tags = vocab[ : idx_i]
    artists = vocab[idx_i : idx_i+idx_j]
    tracks = vocab[idx_i+idx_j : idx_i+idx_j+idx_k]
    audios = vocab[idx_i+idx_j+idx_k : ]
    
    tag_x = x[ : idx_i]
    artist_x = x[idx_i : idx_i+idx_j]
    track_x = x[idx_i+idx_j : idx_i+idx_j+idx_k]
    audio_x = x[idx_i+idx_j+idx_k : ]
    
    tag_y = y[ : idx_i]
    artist_y = y[idx_i : idx_i+idx_j]
    track_y = y[idx_i+idx_j : idx_i+idx_j+idx_k]
    audio_y = y[idx_i+idx_j+idx_k : ]
    return tags, artists, tracks, audios, tag_x, tag_y, artist_x, artist_y, track_x, track_y, audio_x, audio_y, x,y

def _get_umap(tag_embedding,artist_embedding,track_embedding,audio_embedding,fname):
    tag = list(tag_embedding.keys())
    artist = list(artist_embedding.keys())
    track = list(track_embedding.keys())
    audio = ["a_" + i for i in list(audio_embedding.keys())]

    tag_embedding = [emb.reshape(100,) for emb in tag_embedding.values()]
    artist_embedding = list(artist_embedding.values())
    track_embedding = list(track_embedding.values())
    audio_embedding = [emb.reshape(100,) for emb in audio_embedding.values()]

    total_idx = tag+artist+track+audio
    total_emb = np.array(tag_embedding+artist_embedding+track_embedding+audio_embedding)

    print("start tsne",fname)
    embeddings = umap.UMAP(n_neighbors=200,
                      min_dist=0.8,
                      metric='cosine',
                      verbose=1,
                      n_jobs=8).fit_transform(total_emb)
    
    vis_x = embeddings[:, 0]
    vis_y = embeddings[:, 1]
    
    results = {}
    for idx, x, y in zip(total_idx ,vis_x, vis_y):
        results[idx] = {"x":x, "y":y}
    torch.save(results, os.path.join("./umap/",types,fname))
    print("====== save tsne",fname)
    return results


if __name__ == '__main__':
    tag_embedding = torch.load(os.path.join(audio_dir, i))
    artist_embedding = torch.load(os.path.join(artist_dir, i))
    track_embedding = torch.load(os.path.join(track_dir, i))
    audio_embedding = torch.load(os.path.join(audio_dir, i))
    _get_umap(tag_embedding,artist_embedding,track_embedding,audio_embedding,"umap")