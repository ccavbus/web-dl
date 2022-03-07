#!/usr/bin/python3
import os
import requests
from bs4 import BeautifulSoup

def find_video_info(video_id):
    try:
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}
        r = requests.get(f"https://www.javbus.com/{video_id}", headers=header)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find('h3').text.strip()
        poster = "https://www.javbus.com/" + soup.find('div', {'class': 'screencap'}).a['href']
        img = soup.find('div', id='sample-waterfall').find_all('a')
        img_links = [poster]
        for i in img:
            img_links.append(i['href'])
        for i, url in zip(range(len(img_links)), img_links):
            r = requests.get(url, headers=header)
            with open(f"pic{i}.jpg", 'wb') as pic:
                pic.write(r.content)
        print(title, "video info had been saved!")
    except Exception as err:
        print(err, "don't find anything!")

if __name__ == '__main__':
    vid = os.getenv('github.event.inputs.repo')
    find_video_info(vid)