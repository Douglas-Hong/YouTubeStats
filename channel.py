# Author: Douglas Hong
# Version: 12/23/2020
# channel.py


class Channel:
    def __init__(self, channel_data: dict, most_popular_vid_data: dict, channel_id: str) -> None:
        channel_description = channel_data['items'][0]['snippet']
        channel_stats = channel_data['items'][0]['statistics']

        most_popular_vid_description = most_popular_vid_data['items'][0]['snippet']
        most_popular_vid_stats = most_popular_vid_data['items'][0]['statistics']
        
        self._channel_id = channel_id
        self._name = channel_description['title']
        self._creation_date = channel_description['publishedAt'][:10]
        self._subscriber_count = int(channel_stats['subscriberCount'])
        self._view_count = int(channel_stats['viewCount'])
        self._video_count = int(channel_stats['videoCount'])

        self._most_popular_vid_title = most_popular_vid_description['title']
        self._most_popular_vid_date = most_popular_vid_description['publishedAt'][:10]
        self._most_popular_vid_views = int(most_popular_vid_stats['viewCount'])
        self._most_popular_vid_likes = int(most_popular_vid_stats['likeCount'])
        self._most_popular_vid_dislikes = int(most_popular_vid_stats['dislikeCount'])
        self._most_popular_vid_comments = int(most_popular_vid_stats['commentCount'])  


    def channel_id(self) -> str:
        return self._channel_id


    def name(self) -> str:
        return self._name


    def creation_date(self) -> str:
        return self._creation_date


    def subscriber_count(self) -> int:
        return self._subscriber_count


    def view_count(self) -> int:
        return self._view_count


    def video_count(self) -> int:
        return self._video_count


    def average_views_per_video(self) -> int:
        return int(self._view_count / self._video_count)


    def most_popular_vid_title(self) -> str:
        return self._most_popular_vid_title


    def most_popular_vid_date(self) -> str:
        return self._most_popular_vid_date


    def most_popular_vid_views(self) -> int:
        return self._most_popular_vid_views


    def most_popular_vid_likes(self) -> int:
        return self._most_popular_vid_likes


    def most_popular_vid_dislikes(self) -> int:
        return self._most_popular_vid_dislikes


    def most_popular_vid_likes_ratio(self) -> float:
        total_likes = self._most_popular_vid_likes + self._most_popular_vid_dislikes
        return round((self._most_popular_vid_likes / total_likes) * 100, 2)


    def most_popular_vid_comments(self) -> int:
        return self._most_popular_vid_comments

        
