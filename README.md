## Configure

Login Github and go to  account setting to create a peasonal  access token:

Settings -> Developer settings -> Personal access tokens -> Generate new token

And then add the token to the video-dl repo’s secrets

video-dl repo -> setting -> Secrets -> Action secrets -> New repository secret

name: ACCESS_TOKEN

value: content of the token

## BT Downloader

Aria2: Best performent, almost fastest with popular torrent. But it only announce to tracker, so it maybe can not find seeder with unpopular torrent.

qBittorrent: Good performent, mostly slower than aria2 with popular torrent. It can announce to all trackers, so it can download unpopular torrent most of the time.

Transmission: Good performent, mostly slower than aria2 with popular torrent. It can announce to tracker but always failed.