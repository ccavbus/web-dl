#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

tracker_url = "https://trackerslist.com/best_aria2.txt"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'}


def parse_task():
    task = open('task.txt', 'r')
    url = open('url.txt', 'w')
    video = open('video.txt', 'w')
    repo = open('repo.txt', 'w')
    info = task.read().splitlines()
    url.write(info[0])
    video.write(info[1])
    repo.write(info[2])
    task.close()
    url.close()
    repo.close()
    print(info[0], info[1], info[2], "task parsed!")
    return info[2]


def add_tracker(url):
    r = requests.get(url)
    trackers = r.text
    conf = open('aria2.conf', 'a+')
    conf.write(f'bt-tracker={trackers}')
    conf.close()
    print("tracker added!")


def find_video_info(video_id):
    try:
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
    vid = parse_task()
    find_video_info(vid)
    add_tracker(tracker_url)
