import glob
import json
import lzma
from typing import Any, Dict


class InsHashtag:
    def __init__(self, *args):
        '''init Ins class, define its attributes'''
        self.ins_id = args[0]
        self.caption = args[1]
        self.num_comment = args[2]
        self.num_like = args[3]
        self.user_id = args[4]

    def __repr__(self):
        '''to represent Ins as a string
        return: String representation of Ins class '''
        return "{\n Ins id: %s, \n caption: %s, \n num of comment: %s, \n num of likes: %s, \n user_id: %s}" % (
            self.ins_id, self.caption, self.num_comment, self.num_like, self.user_id)

    @classmethod
    def hashtag_from_json(cls, json_obj: Dict[str, Any]):
        ''' select field wanted and convert json object to Ins class
        :param json_obj: json post
        :return ins class object '''

        ins_id = json_obj['node']['id']
        caption = json_obj['node']['edge_media_to_caption']['edges'][0]['node']['text']
        num_comment = json_obj['node']['edge_media_to_comment']['count']
        num_like = json_obj['node']['edge_liked_by']['count']
        user_id = json_obj['node']['owner']['id']
        return InsHashtag(ins_id, caption, num_comment, num_like, user_id)

    def to_document(self) -> Dict[str, Any]:
        '''convert class object to json object in order to store in database
        :return dict object of Ins class '''
        return self.__dict__


class InsProfile:
    def __init__(self, *args):
        '''init Ins class, define its attributes'''
        self.ins_bio = args[0]
        self.num_follower = args[1]
        self.num_following = args[2]
        self.user_name = args[3]
        self.num_reel = args[4]
        self.business = args[5]
        self.professional = args[6]
        self.category_name = args[7]
        self.private = args[8]
        self.verified = args[9]

    def __repr__(self):
        '''to represent Ins as a string
        return: String representation of Ins class '''
        return "{\n Ins bio: %s,  \n num of followers: %s, \n num of following: %s, \n user_name: %s, " \
               "\n num_reel :%s,\n if business :%s, \n if professional :%s, \n category_name :%s,\n if private :%s, \n if verified: %s}" % (
                   self.ins_bio, self.num_follower, self.num_following, self.user_name, self.num_reel, self.business,
                   self.professional, self.category_name, self.private, self.verified)

    @classmethod
    def profile_from_json(cls, json_obj: Dict[str, Any]):
        ''' select field wanted and convert json object to Ins class
        :param json_obj: json post
        :return ins class object '''

        ins_bio = json_obj['node']['biography']
        num_followers = json_obj['node']['edge_followed_by']['count']
        num_following = json_obj['node']['edge_follow']['count']
        user_name = json_obj['node']['full_name']
        num_reel = json_obj['node']['highlight_reel_count']
        business = json_obj['node']['is_business_account']
        professional = json_obj['node']['is_professional_account']
        category_name = json_obj['node']['category_name']
        private = json_obj['node']['is_private']
        verified = json_obj['node']['is_verified']

        return InsProfile(ins_bio, num_followers, num_following, user_name, num_reel, business, professional,
                          category_name, private, verified)

    def to_document(self) -> Dict[str, Any]:
        '''convert class object to json object in order to store in database
        :return dict object of Ins class '''
        return self.__dict__


class InsPost():
    def __init__(self, *args):
        '''init Ins class, define its attributes'''
        self.post_text = args[0]
        self.tagged_user = args[1]
        self.tagged_username = args[2]

    def __repr__(self):
        '''to represent Ins as a string
        return: String representation of Ins class '''
        return "{\n Ins bio: %s,  \n tagged_user: %s, \n tagged_username: %s }" % (
            self.post_text, self.tagged_user, self.tagged_username)

    @classmethod
    def post_from_json(cls, json_obj: Dict[str, Any]):
        ''' select field wanted and convert json object to Ins class
        :param json_obj: json post
        :return ins class object '''

        post_text = json_obj['node']['edge_media_to_caption']['edges'][0]['node']['text']
        check_tagged = json_obj['node']['edge_media_to_tagged_user']['edges']
        if len(check_tagged) != 0:
            tagged_user = json_obj['node']['edge_media_to_tagged_user']['edges'][0]['node']['user']['full_name']
            tagged_username = json_obj['node']['edge_media_to_tagged_user']['edges'][0]['node']['user']['username']
        else:
            tagged_user = '_'
            tagged_username = '_'

        return InsPost(post_text, tagged_user, tagged_username)

    def to_document(self) -> Dict[str, Any]:
        '''convert class object to json object in order to store in database
        :return dict object of Ins class '''
        return self.__dict__

    # def save_json(self, json_name, ls):
    #     '''dump dict into json file'''
    #     with open(json_name+'.json', 'w') as fp:
    #         json.dump(ls, fp)


if __name__ == "__main__":
    hashtag_ls = []
    files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/hashtag/#cat/*.json.xz')
    for file in files:
        with lzma.open(file, "r") as f:
            data = f.read()
            json_obj = json.loads(data.decode('utf-8'))
            inshashtag = InsHashtag.hashtag_from_json(json_obj)
            hash_dict = inshashtag.to_document()
            hashtag_ls.append(hash_dict)
    with open('hashtag_cat.json', 'w') as fp:
        json.dump(hashtag_ls, fp)

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

    post_ls = []
    files = glob.glob('/Users/geminiwenxu/PycharmProjects/Ins/post/selenagomez_*/*.json.xz')
    for file in files:
        with lzma.open(file, "r") as f:
            data = f.read()
            json_obj = json.loads(data.decode('utf-8'))
            inspost = InsPost.post_from_json(json_obj)
            post_dict = inspost.to_document()
            post_ls.append(post_dict)
    with open('selena_post.json', 'w') as fp:
        json.dump(post_ls, fp)

    file = '/Users/geminiwenxu/PycharmProjects/Ins/post/selenagomez_1/2022-05-12_13-45-50_UTC.json.xz'
    with lzma.open(file, "r") as f:
        data = f.read()
        json_obj = json.loads(data.decode('utf-8'))
        inspost = InsPost.post_from_json(json_obj)
        # print(inspost)
