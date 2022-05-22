import os
import pickle
import shutil
import multiprocessing

test_list = pickle.load(open(os.path.join("./MSD_split/filtered_list_test.cP"), 'rb'))
MSD_id_to_7D_id = pickle.load(open(os.path.join("./MSD_split/MSD_id_to_7D_id.pkl"), 'rb'))
id_to_path = pickle.load(open(os.path.join("./MSD_split/7D_id_to_path.pkl"), 'rb'))
msd_id_to_tag_vector = pickle.load(open(os.path.join("./MSD_split/msd_id_to_tag_vector.cP"), 'rb'))
audio_path = "#"

def _copy(msd_id):    
    source = os.path.join(audio_path,id_to_path[MSD_id_to_7D_id[msd_id]])
    target = os.path.join(save_path,id_to_path[MSD_id_to_7D_id[msd_id]])    
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))
    shutil.copy(source,target)

pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-2)
pool.map(_copy, test_list)