import json

import isodate

from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        youtube = Channel.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails, snippet',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        self.title = playlist_videos['items'][0]['snippet']['title'][:24]
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id

    @property
    def total_duration(self):
        total = isodate.parse_duration('PT0M0S')
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration
        return total

    def show_best_video(self):
        likes_count = 0
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > likes_count:
                likes_count = int(video['statistics']['likeCount'])
                video_id = video['id']

        return 'https://youtu.be/' + video_id
