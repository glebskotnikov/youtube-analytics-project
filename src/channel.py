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
        self.url = 'https://www.youtube.com/channel/' + channel_id
        self.subscribercount = channel['items'][0]["statistics"]['subscriberCount']
        self.video_count = channel['items'][0]["statistics"]['videoCount']
        self.viewcount = channel['items'][0]["statistics"]['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscribercount) + int(other.subscribercount)

    def __sub__(self, other):
        return int(self.subscribercount) - int(other.subscribercount)

    def __gt__(self, other):
        return self.subscribercount > other.subscribercount

    def __ge__(self, other):
        return self.subscribercount >= other.subscribercount

    def __lt__(self, other):
        return self.subscribercount < other.subscribercount

    def __le__(self, other):
        return self.subscribercount <= other.subscribercount

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file):
        """
        Метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = {"channel_id": self.channel_id, "title": self.title,
                "description": self.description, "url": self.url,
                "subscribercount": self.subscribercount, "video_count": self.video_count,
                "viewcount": self.viewcount}

        with open(file, 'w') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))
