#!/usr/bin/python3
import requests

def add_tracker(mylist, url):
    r = requests.get(url)
    trackers = ','.join(mylist) + ',' +  r.text
    with open('./aria2/aria2.conf', 'a+') as f:
        f.write(f'bt-tracker={trackers}')
    print("tracker added!")


if __name__ == '__main__':
    mylist = ["http://sukebei.tracker.wf:8888/announce",
              "http://tracker.bt4g.com:2095/announce"]
<<<<<<< HEAD
    url = "https://ngosang.github.io/trackerslist/trackers_best.txt"
    add_tracker(mylist, url)
=======
    url = "https://trackerslist.com/best_aria2.txt"
    add_tracker(mylist, url)
>>>>>>> parent of a7c798a (Update add_tracker.py)
