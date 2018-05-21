import opml
import feedparser
import youtube_dl
import time
import datetime

class subscription_download_manager():
    def __init__(self, subscription_manager_file):
        self.file = subscription_manager_file
        self.parsed = opml.parse(self.file)
        self.channels = self.get_channels()
        self.channels_cached_list = []

    def get_channels(self):
        channels = []
        for c in range(0, len(self.parsed[0])):
            channels.append(self.parsed[0][c].xmlUrl)
        return channels

    def populate_channel_cache(self, check=False):
        if len(self.channels_cached_list) == 0 or check:
            channel_list = []
            for c in self.channels:
                feed = feedparser.parse(c)
                self.channels_cached_list.append(feed)

    def get_videos(self, check=False, since=None, download=False, ydl_opts={}):
        videos = []
        self.populate_channel_cache(check)
        links = self.get_videos_attrs('link')
        if since != None:
            current_time = time.time()
            videos_since = current_time - since
            dates = self.get_videos_attrs('published_parsed')
            for l in range(0,len(links)):
                if time.mktime(dates[l]) > videos_since:
                    videos.append(links[l])
        else:
            for l in links:
                videos.append(l)
        if download == True:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(videos)
        return videos

    def get_videos_attrs(self, attr, check=False):
        l = []
        self.populate_channel_cache(check)
        for channel_feed in self.channels_cached_list:
            for i in channel_feed['items']:
                l.append(i[attr])
        return l

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="subscription manager xml file obtained from youtube", type=str, default='subscription_manager')
    parser.add_argument("--since", help="Download videos since (time in seconds) Ex: -s 86400 would download videos from up to one day ago", default=86400, type=float)
    parser.add_argument("--output", help="Directory to download videos. Default: ~/Downloads/", default='~/Downloads')
    args = parser.parse_args()
    ydl_opts = {
            'outtmpl': args.output + '/%(title)s.%(ext)s',
            }
    m = subscription_download_manager(args.config)
    m.get_videos(since=args.since, download=True, ydl_opts=ydl_opts)
