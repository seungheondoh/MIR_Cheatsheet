#-*- coding: utf-8 -*-

from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import re
import json
import os
from selenium.webdriver.chrome.options import Options
import random

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def _title_filter(title):
    binary = 1
    nlp_filter = ['vlog', 'official','episode']
    delete_keys = []
    for token in nlp_filter:
        if token in title.lower():
            binary = 0
    return binary
    
def _get_urls(keyword, code, results, TIME_SLEEP):
    if code == "en":
        keyword = keyword + " music"
    elif code == "ko":
        keyword = keyword + " 음악"
    elif code == "fr":
        keyword = keyword + " musique"
    search_keyword_encode = keyword + ' "playlist"'
    url = "https://www.youtube.com/results?search_query=" + search_keyword_encode
    driver = wd.Chrome(executable_path="./chromedriver", options=chrome_options)
    driver.get(url)
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(TIME_SLEEP)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    datas = soup.select("a#video-title")

    for data in datas:
        title = data.text.replace('\n', '')
        url = "https://www.youtube.com" + data.get('href')
        results[url] = title
    driver.quit()
    return results

def main(keyword, code):
    results = {}
    MAX_LENGTH = 300
    TIME_SLEEP = 3.0
    count = 0

    while len(results) < MAX_LENGTH:
        print("iter: ", count, "Time Sleep: ", TIME_SLEEP, "length: ", len(results))
        results = _get_urls(keyword, code, results, TIME_SLEEP)
        TIME_SLEEP = TIME_SLEEP + 5.0
        count = count + 1
        if count > 3:
            break
    
    return results

if __name__ == "__main__":
    save_dir = '../dataset/query'
    query_set = json.load(open("../dataset/query/query_set.json", 'r', encoding='utf-8'))
    print("start!")
    for q in query_set.keys():
        countries = query_set[q]
        for i in countries.keys():
            print("query is ", q, "country is ", i)
            results = main(countries[i], i)
            save_path = os.path.join(save_dir, q, i + ".json")
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            with open(save_path, "w", encoding='utf-8') as file_write:
                json.dump(results, file_write, indent=4, ensure_ascii=False)
    