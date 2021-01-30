# Author: Douglas Hong
# Version: 12/23/2020
# youtube_stats_ui.py


from youtube_channels import YouTubeChannels


class YouTubeChannelsStats:
    def __init__(self):
        #
        # # Most recent video??? Put commands on numbers?
        # Add option to calculate mean subscribers/views and total views of channel list
        # Add compare statistics command and ask user what stat they want to use
        # Google Maps API?
        # Upload to GitHub
        #
        self._channels = YouTubeChannels(self._get_api_key())


    def run(self):
        while True:
            self._print_commands()
            command = input().strip()

            if command == '1':
                self._add_channel()

            elif command == '2':
                self._print_channel_stats()

            elif command == '3':
                self._sort_channel_list()

            elif command == '4':
                self._delete_channel()

            elif command == '5':
                self._print_channel_list_stats()

            elif command == '6':
                break

            else:
                print('That is an invalid command')
                continue

            self._print_channel_names()


    def _add_channel(self) -> None:
        channel_url = input("Enter the YouTube channel's URL: ").strip()
        channel_id = channel_url[channel_url.rfind('/') + 1:]
        self._channels.add_channel(channel_id)


    def _delete_channel(self) -> None:
        channel_name = input('Enter the name of the channel to delete: ').strip()
        self._channels.delete_channel(channel_name)


    def _print_channel_stats(self) -> None:
        channel_name = input('Enter the name of the channel: ').strip()
        
        for channel in self._channels.channel_list():
            if channel.name().casefold() == channel_name.casefold():
                print()
                print('Channel name: ' + channel.name())
                print('Creation date: ' + channel.creation_date())
                print('Subscriber count:', channel.subscriber_count())
                print('View count:', channel.view_count())
                print('Video count:', channel.video_count())
                print('Average views per video:', channel.average_views_per_video())
                print()
                print('Most popular video title: ' + channel.most_popular_vid_title())
                print('Most popular video publish date: ' + channel.most_popular_vid_date())
                print('Most popular video view count:', channel.most_popular_vid_views())
                print('Most popular video likes/dislikes:', channel.most_popular_vid_likes(),
                      '/', channel.most_popular_vid_dislikes(),
                      '(' + str(channel.most_popular_vid_likes_ratio()) + '% likes)')
                print('Most popular video comment count:', channel.most_popular_vid_comments())
                break


    def _print_channel_list_stats(self) -> None:
        channel_list = self._channels.channel_list()

        subscriber_sum = sum([ch.subscriber_count() for ch in channel_list])
        view_count_sum = sum([ch.view_count() for ch in channel_list])
        creation_date_sort = sorted(channel_list, key = lambda ch: ch.creation_date())
        like_ratio_sort = sorted(channel_list, key = lambda ch: ch.most_popular_vid_likes_ratio())

        print()
        print('Mean subscribers:', int(subscriber_sum / len(channel_list)))
        print('Mean view count:', int(view_count_sum / len(channel_list)))
        print('Total subscribers:', subscriber_sum)
        print('Total view count:', view_count_sum)
        print('Oldest channel:', creation_date_sort[0].name())
        print('Newest channel:', creation_date_sort[-1].name())
        print('Most popular video:',
              sorted(channel_list, key = lambda ch: ch.most_popular_vid_views())[-1].most_popular_vid_title())
        print('Highest like ratio (based on most popular video):', like_ratio_sort[-1].name(),
              '(' + str(like_ratio_sort[-1].most_popular_vid_likes_ratio()) + '% likes)')
        print('Lowest like ratio (based on most popular video):', like_ratio_sort[0].name(),
              '(' + str(like_ratio_sort[0].most_popular_vid_likes_ratio()) + '% likes)')
        print('Most commented video (based on most popular video):',
              sorted(channel_list, key = lambda ch: ch.most_popular_vid_comments())[-1].most_popular_vid_title())
        


    def _sort_channel_list(self) -> None:
        self._print_sorting_commands()
        command = input().strip()

        if command == '1': self._channels.sort_by_name(reverse = False)

        elif command == '2': self._channels.sort_by_name(reverse = True)
            
        elif command == '3': self._channels.sort_by_subscribers(reverse = True)

        elif command == '4': self._channels.sort_by_subscribers(reverse = False)
        
        elif command == '5': self._channels.sort_by_views(reverse = True)

        elif command == '6': self._channels.sort_by_views(reverse = False)

        elif command != '7': print('Invalid command')


    def _print_channel_names(self) -> None:
        channel_list = self._channels.channel_list()
        
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


    def _get_api_key(self) -> str:
        while True:
            file_path = input('Enter the path to the text file with your API key: ').strip()

            try:
                api_key = open(file_path).readline().rstrip('\n')

            except (ValueError, OSError):
                print('That is an invalid API key')

            else:
                return api_key


    def _print_commands(self) -> None:
        print()
        print('-----------------------------------------------------------------')
        print('What would you like to do?')
        print('Enter the number of the command you want to execute; example: "1"')
        print('-----------------------------------------------------------------')
        print('1: Add a channel to my channel list')
        print('2: Review the statistics of one channel in my channel list')
        print('3: Sort my channel list')
        print('4: Remove channel from my channel list')
        print('5: Review the statistics of my whole channel list')
        print('6: QUIT PROGRAM')
        print()


    def _print_sorting_commands(self) -> None:
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


if __name__ == '__main__':
    YouTubeChannelsStats().run()
