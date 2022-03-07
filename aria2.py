#!/usr/bin/python3
import requests

def add_tracker(url):
    r = requests.get(url)
    trackers = r.text
    conf = open('aria2.conf', 'a+')
    conf.write(f'bt-tracker={trackers}')
    conf.close()
    print("tracker added!")


if __name__ == '__main__':
    url = "https://trackerslist.com/best_aria2.txt"
    add_tracker(url)