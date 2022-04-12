#!/usr/bin/python3
import requests

def add_tracker(mylist, url):
    r = requests.get(url)
    trackers = ','.join(mylist) + ',' +  r.text
    conf = open('aria2.conf', 'a+')
    conf.write(f'bt-tracker={trackers}')
    conf.close()
    with open('aria2.conf') as f:
        print(f.read())
    print("tracker added!")


if __name__ == '__main__':
    mylist = ["http://sukebei.tracker.wf:8888/announce",
              "http://tracker.bt4g.com:2095/announce"]
    url = "https://trackerslist.com/best_aria2.txt"
    add_tracker(mylist, url)