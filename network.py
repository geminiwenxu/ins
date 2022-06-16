import glob
import json
import lzma

from extract import extract_user, extract_hashtag
from read import InsHashtag

if __name__ == "__main__":
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
        if answer == 'selena':
            name = 'selena'
            f = open(name + '_post.json')
            post = json.load(f)
            for i in post:
                print(i['post_text'])
                if i['tagged_username'] != "_":
                    print((i['tagged_user']))
                    print('do you want to download info about this user')
                    answer = input()
                    if answer == 'y':
                        extract_user()
                    else:
                        print('ok')
                print('________________________________')
        elif answer == 'geeks_for_geeks':
            name = 'geeks_for_geeks'
            f = open(name + '_post.json')
            post = json.load(f)
            for i in post:
                print(i['post_text'])
                print('________________________________')
        else:
            print("enter the user you want to explore")
            answer = input()
            extract_user()
    else:
        print('which hashtag would you like to explore?')
        answer = input()
        files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/#' + answer + '/*.json.xz')
        for file in files:
            with lzma.open(file, "r") as f:
                data = f.read()
                json_obj = json.loads(data.decode('utf-8'))
                inshashtag = InsHashtag.hashtag_from_json(json_obj)
                hash_dict = inshashtag.to_document()
                print(hash_dict)



