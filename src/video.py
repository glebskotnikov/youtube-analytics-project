from src.channel import Channel


class Video:

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        youtube = Channel.get_service()
        try:
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            self.video_id = video_id
            self.title = video_response['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/watch?v=' + video_id
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.video_id})'

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Второй класс для видео, который инициализируется 'id видео' и 'id плейлиста
    '"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id