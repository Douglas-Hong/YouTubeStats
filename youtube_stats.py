# Author: Douglas Hong
# Version: 12/23/2020
# youtube_stats.py


import json
import urllib.parse
import urllib.request
from channel import Channel
from datetime import datetime


def run() -> None:
    api_key = get_api_key()
    channel_list = []

    while True:
        print_commands()
        command = input().strip()

        if command == '1':
            add_channel(api_key, channel_list)

        elif command == '2':
            channel_name = input('Enter the name of the channel: ').strip()
            print_channel_details(channel_list, channel_name)

        elif command == '3':
            sort_channel_list(channel_list)

        elif command == '4':
            delete_channel(channel_list)

        elif command == '5':
            break

        else:
            print('That is an invalid command')
            continue

        print_channel_names(channel_list)
    

def get_api_key() -> str:
    while True:
        file_path = input('Enter the path to the text file with your API key: ').strip()

        try:
            api_key = open(file_path).readline().rstrip('\n')

        except (ValueError, OSError):
            print('That is an invalid API key')

        else:
            return api_key 


def print_commands() -> None:
    print()
    print('-----------------------------------------------------------------')
    print('What would you like to do?')
    print('Enter the number of the command you want to execute; example: "1"')
    print('-----------------------------------------------------------------')
    print('1: Add a channel to my channel list')
    print('2: Review the statistics of one channel in my channel list')
    print('3: Sort my channel list')
    print('4: Remove channel from my channel list')
    print('5: QUIT PROGRAM')
    print()


def add_channel(api_key: str, channel_list: [str]) -> None:
    channel_url = input("Enter the YouTube channel's URL: ").strip()
    channel_id = channel_url[channel_url.rfind('/') + 1:]  
    channel_data = get_data(build_channel_data_url(api_key, channel_id))
    
    most_popular_vid_id = get_data(build_most_popular_vid_url(api_key, channel_id))['items'][0]['id']['videoId']
    most_popular_vid_data = get_data(build_most_popular_vid_data(api_key, most_popular_vid_id))
    
    channel_list.append(Channel(channel_data, most_popular_vid_data, channel_id))


def delete_channel(channel_list: [str]) -> None:
    channel = input('Enter the name of the channel to delete: ').strip()

    for i in range(len(channel_list)):
        if channel_list[i].name().casefold() == channel.casefold():
            del channel_list[i]


def build_channel_data_url(api_key: str, channel_id: str) -> str:
    query_parameters = [('part', 'statistics, snippet'), ('id', channel_id), ('key', api_key)]

    return BASE_YOUTUBE_URL + '/channels?' + urllib.parse.urlencode(query_parameters)


def build_most_popular_vid_url(api_key: str, channel_id: str) -> str:
    query_parameters = [('part', 'snippet'), ('channelId', channel_id), ('key', api_key),
                        ('order', 'viewCount'), ('type', 'video'), ('maxResults', 10),
                        ('safeSearch', 'none')]

    return BASE_YOUTUBE_URL + '/search?' + urllib.parse.urlencode(query_parameters)


def build_most_popular_vid_data(api_key: str, video_id: str) -> str:
    query_parameters = [('part', 'statistics,snippet'), ('id', video_id), ('key', api_key)]

    return BASE_YOUTUBE_URL + '/videos?' + urllib.parse.urlencode(query_parameters)
                        

def get_data(url: str) -> dict:
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


def print_channel_names(channel_list: [Channel]) -> None:
    print()
    print('Your current channel list: ')
    print()

    print(' No. |          Name          |  Subscribers  |  Total Views  |')
    print('-----|------------------------|---------------|---------------|')
    
    for i in range(len(channel_list)):
        name = channel_list[i].name()
        subscribers = str(channel_list[i].subscriber_count())
        views = str(channel_list[i].view_count())

        print(str(i + 1) + (' ' * (len(' No. ') - len(str(i + 1)))), end = '|')
        print(name + (' ' * (len('          Name          ') - len(name))), end = '|')
        print(subscribers + (' ' * (len('  Subscribers  ') - len(subscribers))), end = '|')
        print(views + (' ' * (len('  Total Views  ') - len(views))), end = '|\n')

        if i == len(channel_list) - 1:
            print('---------------------------------------------------------------')
        else:
            print('-----|------------------------|---------------|---------------|')
        

def print_channel_details(channel_list: [Channel], channel_name: str) -> None:
    for channel in channel_list:
        if channel.name().casefold() == channel_name.casefold():
            print('Channel name: ' + channel.name())
            print('Creation date: ' + channel.creation_date())
            print('Subscriber count:', channel.subscriber_count())
            print('View count:', channel.view_count())
            print('Video count:', channel.video_count())
            print()
            print('Most popular video title: ' + channel.most_popular_vid_title())
            print('Most popular video publish date: ' + channel.most_popular_vid_date())
            print('Most popular video view count:', channel.most_popular_vid_views())
            print('Most popular video likes/dislikes:', channel.most_popular_vid_likes(),
                  '/', channel.most_popular_vid_dislikes(),
                  '(' + str(channel.most_popular_vid_likes_ratio()) + '% likes)')
            print('Most popular video comment count:', channel.most_popular_vid_comments())
            break

    else:
        print(channel_name + ' is not in your channel list')


def print_sorting_commands() -> None:
    print()
    print('-----------------------------------------------------------------')
    print('How would you like to sort your channel list?')
    print('Enter the number of the command you want to execute; example: "1"')
    print('-----------------------------------------------------------------')
    print('1: ABC order (from A to Z)')
    print('2: Reverse ABC order (from Z to A)')
    print('3: Most subscribers to least subscribers')
    print('4: Least subscribers to most subscribers')
    print('5: Most views to least views')
    print('6: Least views to most views')
    print('7: QUIT SORTING')
    print()
    

def sort_channel_list(channel_list: [Channel]) -> None:
    print_sorting_commands()
    command = input().strip()

    if command == '1': channel_list.sort(key = (lambda channel: channel.name()))

    elif command == '2': channel_list.sort(key = (lambda channel: channel.name()), reverse = True)

    elif command == '3': channel_list.sort(key = (lambda channel: channel.subscriber_count()), reverse = True)

    elif command == '4': channel_list.sort(key = (lambda channel: channel.subscriber_count()))

    elif command == '5': channel_list.sort(key = (lambda channel: channel.view_count()), reverse = True)

    elif command == '6': channel_list.sort(key = (lambda channel: channel.view_count()))

    elif command != '7': print('Invalid command')

        
if __name__ == '__main__':
    run()
