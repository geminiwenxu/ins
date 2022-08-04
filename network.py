import glob
import json
import lzma
import shutil

from extract import extract_user, extract_hashtag
from read import InsProfile, InsPost


def move(Username):
    # Move files
    profile_folder = r'/Users/geminiwenxu/PycharmProjects/Ins/' + Username + '/'
    target = r'/Users/geminiwenxu/PycharmProjects/Ins/profile'
    shutil.move(profile_folder, target)
    post_folder = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/' + Username + '_*')
    target = r'/Users/geminiwenxu/PycharmProjects/Ins/post'
    for i in post_folder:
        name = i[39:]
        original = r'/Users/geminiwenxu/PycharmProjects/Ins/' + name + '/'
        shutil.move(original, target)
    # Read files and generate files
    profile_ls = []
    files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/profile/*/*.json.xz')
    for file in files:
        with lzma.open(file, "r") as f:
            data = f.read()
            json_obj = json.loads(data.decode('utf-8'))
            insprofile = InsProfile.profile_from_json(json_obj)
            profile_dict = insprofile.to_document()
            profile_ls.append(profile_dict)
    with open('profile.json', 'w') as fp:
        json.dump(profile_ls, fp)


if __name__ == "__main__":
    user_ls = ['Selena Gomez', 's1070771', 'Justin Bieber', 'Netflix DE', 'Wondermind', 'GeeksforGeeks', 'disney',
               'Saturday Night Live', 'Rare Beauty by Selena Gomez']
    print('Would like to start to explore by user or by hashtag?')
    answer = input()
    if answer == 'user':
        f = open('profile.json')
        data = json.load(f)
        for i in data:
            user_name = i['user_name']
            print(user_name)
        print('which user post caption you would like to see?')
        answer = input()
        name = answer
        if any(answer in s for s in user_ls):
            files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/profile/' + name + '/*.json.xz')
            for file in files:
                with lzma.open(file, "r") as f:
                    data = f.read()
                    json_obj = json.loads(data.decode('utf-8'))
                    insprofile = InsProfile.profile_from_json(json_obj)
                    profile_dict = insprofile.to_document()
                    print('User profile: ', profile_dict)

                    # read this user's post and generate post.json file
                    print('Do you want to further explore this user post?')
                    answer = input()
                    if answer == 'yes':
                        post_ls = []
                        files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/post/' + name + '_*/*.json.xz')
                        for file in files:
                            with lzma.open(file, "r") as f:
                                data = f.read()
                                json_obj = json.loads(data.decode('utf-8'))
                                inspost = InsPost.post_from_json(json_obj)
                                post_dict = inspost.to_document()
                                post_ls.append(post_dict)
                        with open(name + '_post.json', 'w') as fp:
                            json.dump(post_ls, fp)
                        # exploring the post of this user
                        for file in files:
                            f = open(name + '_post.json')
                            post = json.load(f)
                            for i in post:
                                print(i['post_text'])
                                if i['tagged_username'] != "_":
                                    Username = i['tagged_username']
                                    print(('tagged_user: ', i['tagged_user']))

                                    print('Do you want to download info about this user')
                                    answer = input()
                                    if answer == 'yes':
                                        extract_user(Username)
                                        move(Username)
                                        user_ls.extend(Username)

                                        # generating new profile.json
                                        profile_ls = []
                                        files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/profile/*/*.json.xz')
                                        for file in files:
                                            with lzma.open(file, "r") as f:
                                                data = f.read()
                                                json_obj = json.loads(data.decode('utf-8'))
                                                insprofile = InsProfile.profile_from_json(json_obj)
                                                profile_dict = insprofile.to_document()
                                                profile_ls.append(profile_dict)
                                        with open('profile.json', 'w') as fp:
                                            json.dump(profile_ls, fp)
                                    else:
                                        print('ok, next post--------------------->')
        else:
            print("enter the user you want to explore")
            Username = input()
            extract_user(Username)  # but once extract user, program stops !!!!!!!!!

    else:
        print('do you want to explore the existing hashtag?')
        answer = input()
        if answer == 'yes':
            f = open('hashtag.json')
            hashtag = json.load(f)
            for i in hashtag:
                print('ins_id: ', i['ins_id'])
                print('caption: ', i['caption'])
                print('number of comments:', i['num_comment'])
                print('number of likes: ', i['num_like'])
                print('user_id: ', i['user_id'])
                print('---------------------------------------------------------')
        else:
            print('which hashtag would you like to explore?')
            tag = input()
            extract_hashtag(tag)
