import json
import os
import youtube_dl
import wget
import argparse

parser = argparse.ArgumentParser(description='thumbnail/meta crawling')
parser.add_argument('-t_dir', type=str, default='../dataset/thumbnail')
parser.add_argument('-m_dir', type=str, default='../dataset/meta')

def crawl(url, audio_out_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'writeinfojson': False,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': audio_out_dir
    }
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download = False)
    return meta

def _get_meta_dict(meta, url):
    meta_dict = {}
    meta_dict['url'] = url
    meta_dict['title'] = meta['title']
    meta_dict['thumbnail'] = meta['thumbnail']
    meta_dict['categories'] = meta['categories']
    meta_dict['duration'] = meta['duration'] / 60
    meta_dict['tags'] = meta['tags']
    meta_dict['description'] = meta['description']
    return meta_dict

def _duration_filter(duration):
    binary = 1
    if duration < 20:
        binary = 0
    return binary
    
def _title_filter(title):
    binary = 1
    nlp_filter = ['vlog',"movie",'official','episode','브이로그','video',"album", "english", "feat","lyrics", "version", "season", "kid"]
    delete_keys = []
    for token in nlp_filter:
        if token in title.lower():
            binary = 0
    return binary

def main():
    args = parser.parse_args()
    urls_dir = "../dataset/query"
    lang = ['en.json', 'ko.json', 'fr.json']
    errros = []
    for (root, dirs, files) in os.walk(urls_dir):
        for dir_name in dirs:
            print("start: ",dir_name)
            for la in lang:
                urls_dict = json.load(open(os.path.join(root, dir_name, la), 'r', encoding='utf-8')).keys()
                for url in urls_dict:
                    if "list" in url:
                        pass
                    else:
                        try:
                            meta = crawl(url, "./")
                            meta_dict = _get_meta_dict(meta, url)
                            if _duration_filter(meta_dict['duration']) and _title_filter(meta_dict['title']):
                                ids = meta['id']
                                thumb_url = meta['thumbnail']
                                thumb_path = os.path.join(args.t_dir, dir_name, la.split(".json")[0] ,ids + ".jpg")
                                meta_path = os.path.join(args.m_dir, dir_name, la.split(".json")[0] ,ids + ".json")
                                
                                if not os.path.exists(os.path.dirname(meta_path)):
                                    os.makedirs(os.path.dirname(meta_path))
                                if os.path.isfile(meta_path) == 1:
                                    print(meta_path + '_file_already_extracted!')
                                else:
                                    with open(meta_path, "w", encoding='utf-8') as file_write:
                                        json.dump(meta_dict, file_write, indent=4, ensure_ascii=False)

                                if not os.path.exists(os.path.dirname(thumb_path)):
                                    os.makedirs(os.path.dirname(thumb_path))
                                if os.path.isfile(thumb_path) == 1:
                                    print(thumb_path + '_file_already_extracted!')
                                else:
                                    wget.download(thumb_url, thumb_path)
                        except:
                            errros.append(url)
    
if __name__ == '__main__':
    main()