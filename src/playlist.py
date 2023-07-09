import datetime
import json

import isodate

from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        youtube = Channel.get_service()
        playlist = youtube.playlists().list(id=playlist_id,
                                            part='contentDetails, snippet',
                                            maxResults=50,
                                            ).execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails, snippet',
                                                            maxResults=50,
                                                            ).execute()['items']

    @property
    def total_duration(self):
        youtube = Channel.get_service()
        total = datetime.timedelta()
        for pl_video in self.playlist_videos:
            video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=pl_video['contentDetails']['videoId']
                                          ).execute()['items'][0]
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        youtube = Channel.get_service()
        likes_count = 0
        for pl_video in self.playlist_videos:
            video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=pl_video['contentDetails']['videoId']
                                          ).execute()['items'][0]
            if int(video['statistics']['likeCount']) > likes_count:
                likes_count = int(video['statistics']['likeCount'])
                video_id = video['id']

        return 'https://youtu.be/' + video_id
