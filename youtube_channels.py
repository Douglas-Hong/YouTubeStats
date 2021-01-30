# Author: Douglas Hong
# Version: 12/25/2020
# youtube_channels.py


import json
import urllib.parse
import urllib.request
from channel import Channel


BASE_YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3'


class YouTubeChannels:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._channel_list = []


    def channel_list(self) -> [str]:
        return self._channel_list[:]


    def add_channel(self, channel_id: str) -> None:
        channel_data = self._get_data(self._build_channel_data_url(channel_id))
        most_popular_vid_id = self._get_data(self._build_most_popular_vid_url(channel_id))['items'][0]['id']['videoId']
        most_popular_vid_data = self._get_data(self._build_most_popular_vid_data(most_popular_vid_id))

        self._channel_list.append(Channel(channel_data, most_popular_vid_data, channel_id))


    def delete_channel(self, channel_name: str) -> None:
        for i in range(len(self._channel_list)):
            if self._channel_list[i].name().casefold() == channel_name.casefold():
                del self._channel_list[i]
                break


    def sort_by_name(self, reverse: bool) -> None:
        self._channel_list.sort(key = lambda channel: channel.name(), reverse = reverse)


    def sort_by_subscribers(self, reverse: bool) -> None:
        self._channel_list.sort(key = lambda channel: channel.subscriber_count(), reverse = reverse)


    def sort_by_views(self, reverse: bool) -> None:
        self._channel_list.sort(key = lambda channel: channel.view_count(), reverse = reverse)
        

    def _build_channel_data_url(self, channel_id: str) -> str:
        query_parameters = [('part', 'statistics, snippet'), ('id', channel_id), ('key', self._api_key)]

        return BASE_YOUTUBE_URL + '/channels?' + urllib.parse.urlencode(query_parameters)


    def _build_most_popular_vid_url(self, channel_id: str) -> str:
        query_parameters = [('part', 'snippet'), ('channelId', channel_id), ('key', self._api_key),
                            ('order', 'viewCount'), ('type', 'video'), ('maxResults', 10),
                            ('safeSearch', 'none')]

        return BASE_YOUTUBE_URL + '/search?' + urllib.parse.urlencode(query_parameters)


    def _build_most_popular_vid_data(self, video_id: str) -> str:
        query_parameters = [('part', 'statistics,snippet'), ('id', video_id), ('key', self._api_key)]

        return BASE_YOUTUBE_URL + '/videos?' + urllib.parse.urlencode(query_parameters)


    def _get_data(self, url: str) -> dict:
        '''
        This function takes a URL and returns a Python dictionary representing the
        parsed JSON response.
        '''
        response = None

        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
            return json.loads(json_text)

        finally:
            if response != None:
                response.close()
