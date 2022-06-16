import instaloader
from instaloader import Hashtag


def extract_hashtag():
    HASHTAG = input('Enter the Hashtag: ')
    bot = instaloader.Instaloader()
    print(bot.context)
    hashtag = Hashtag.from_name(bot.context, HASHTAG)
    for post in hashtag.get_posts():
        bot.download_post(post, target="#" + hashtag.name)


def extract_user():
    Username = input('Enter the Account Username: ')
    bot = instaloader.Instaloader()
    bot.download_profile(Username, profile_pic_only=True)
    profile = instaloader.Profile.from_username(bot.context, Username)
    print("Username: ", profile.username)
    print("User ID: ", profile.userid)
    print("Number of Posts: ", profile.mediacount)
    print("Followers: ", profile.followers)
    print("Followees: ", profile.followees)
    print("Bio: ", profile.biography, profile.external_url)

    posts = profile.get_posts()
    try:
        for index, post in enumerate(posts, 1):
            bot.download_post(post, target=f"{profile.username}_{index}")
    except:
        exit()


def extract_user_id():
    USERID = input('Enter the Account User ID: ')
    L = instaloader.Instaloader()
    # USER = "s1070771"
    # PASSWORD = "s1070771pw"
    # L.login(USER, PASSWORD)  # (login)
    # L.interactive_login(USER)  # (ask password on terminal)
    # L.load_session_from_file(USER)  # (load session created w/

    Username = instaloader.Profile.from_id(L.context, USERID).username
    profile = instaloader.Profile.from_username(L.context, Username)
    posts = profile.get_posts()
    try:
        for index, post in enumerate(posts, 1):
            L.download_post(post, target=f"{profile.username}_{index}")
    except:
        exit()


if __name__ == "__main__":
    extract_hashtag()
