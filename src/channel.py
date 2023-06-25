import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel_id
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']["thumbnails"]["default"]["url"]
        self.subscribercount = channel['items'][0]["statistics"]['subscriberCount']
        self.video_count = channel['items'][0]["statistics"]['videoCount']
        self.viewcount = channel['items'][0]["statistics"]['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file):
        data = {"channel_id": self.channel_id, "title": self.title,
                "description": self.description, "url": self.url,
                "subscribercount": self.subscribercount, "video_count": self.video_count,
                "viewcount": self.viewcount}

        with open(file, 'w') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
