from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader
from instaloader import Hashtag


def extract_hastag_date():
    # Use parameters to save diffrent metadata
    L = instaloader.Instaloader(download_pictures=True, download_videos=False, download_comments=False,
                                save_metadata=True)

    # Login
    username = input("Enter your username: ")
    L.interactive_login(username=username)

    # User Query
    search = input("Enter Hashtag: ")
    limit = int(input("How many posts to download: "))

    # Hashtag object
    hashtags = instaloader.Hashtag.from_name(L.context, search).get_posts()

    # Download Period
    SINCE = datetime(2021, 5, 1)
    UNTIL = datetime(2021, 3, 1)

    no_of_downloads = 0
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, hashtags)):
        if no_of_downloads == limit:
            break
        print(post.date)
        L.download_post(post, "#" + search)
        no_of_downloads += 1


def extract_hashtag(HASHTAG):
    bot = instaloader.Instaloader()
    hashtag = Hashtag.from_name(bot.context, HASHTAG)
    for post in hashtag.get_posts():
        bot.download_post(post, target="#" + hashtag.name)


def extract_user(Username):
    bot = instaloader.Instaloader()
    bot.download_profile(Username, profile_pic_only=True)
    profile = instaloader.Profile.from_username(bot.context, Username)
    posts = profile.get_posts()
    try:
        for index, post in enumerate(posts, 1):
            bot.download_post(post, target=f"{profile.username}_{index}")
    except Exception as ex:
        # exit() #### modify here
        print(f"error happens here {ex}")


def extract_user_id():
    USERID = input('Enter the Account User ID: ')
    bot = instaloader.Instaloader()
    Username = instaloader.Profile.from_id(bot.context, USERID).username
    profile = instaloader.Profile.from_username(bot.context, Username)
    posts = profile.get_posts()
    try:
        for index, post in enumerate(posts, 1):
            bot.download_post(post, target=f"{profile.username}_{index}")
    except Exception as ex:
        print(f"error happens here {ex}")


class Extract():
    def __init__(self):
        self.bot = instaloader.Instaloader()

    def extract_user(self):
        Username = input('Enter the Account Username: ')
        self.bot.download_profile(Username, profile_pic_only=True)
        profile = instaloader.Profile.from_username(self.bot.context, Username)
        posts = profile.get_posts()
        try:
            for index, post in enumerate(posts, 1):
                self.bot.download_post(post, target=f"{profile.username}_{index}")
        except Exception as ex:
            print(f"error happens here {ex}")

    def extract_user_id(self):
        USERID = input('Enter the Account User ID: ')
        Username = instaloader.Profile.from_id(self.bot.context, USERID).username
        profile = instaloader.Profile.from_username(self.bot.context, Username)
        posts = profile.get_posts()
        try:
            for index, post in enumerate(posts, 1):
                self.bot.download_post(post, target=f"{profile.username}_{index}")
        except Exception as ex:
            print(f"error happens here {ex}")

    def extract_hashtag(self):
        HASHTAG = input('Enter the Hashtag: ')
        hashtag = Hashtag.from_name(self.bot.context, HASHTAG)
        for post in hashtag.get_posts():
            self.bot.download_post(post, target="#" + hashtag.name)


if __name__ == "__main__":
    test = Extract()
    test.extract_user()
