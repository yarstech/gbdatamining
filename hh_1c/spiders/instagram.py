# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib.parse import urlencode, urljoin
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    graphql_url = 'https://instagram.com/graphql/query/?'
    variables_base = {"include_reel":'true', "fetch_mutual": 'false', "first": 100}

    variables_post_base = {"child_comment_count": 10, "fetch_comment_count": 10,
                           "parent_comment_count": 10, "has_threaded_comments": 'true'}

    p_users = {}


    def __init__(self, login, pwd, users, *args, **kwargs):
        self.login = login
        self.pwd = pwd
        self.users = users
        self.query_hash = 'd04b0a864b4b54837c0d870b0e77e076'
        self.query_post_hash = 'fead941d698dc1160a298ba7bec277ac'
        super().__init__(*args, **kwargs)

    def parse(self, response):
        csrf_token = self.fetch_csrf_token(response.text)
        inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

        yield scrapy.FormRequest(
            inst_login_link,
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.pwd},
            headers={'X-CSRFToken': csrf_token}
        )

        print(1)

    def parse_users(self, response):
        j_body = json.loads(response.body)
        if j_body.get('authenticated'):
            for user in self.users:
                yield response.follow(urljoin(self.start_urls[0], user),
                                      callback=self.parse_user,
                                      cb_kwargs={'user':user})


    def parse_user(self, response, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})

        yield response.follow(self.make_graphql_url(user_vars),
                              callback=self.parse_following,
                              cb_kwargs={'user_vars': user_vars, 'user': user}
                              )

        print(1)

    def parse_following(self, response, user_vars, user):
        data = json.loads(response.body)

        if not self.p_users.get(user):
            self.p_users[user] = {}

        if not self.p_users[user].get('following'):
            self.p_users[user]['following'] = {}

        #self.p_users[user]['edges'].extend(data['data']['user']['edge_follow']['edges'])
        #self.p_users[user] = {'edges': data['data']['user']['edge_follow']['edges']}


        for foll_user in data['data']['user']['edge_follow']['edges']:
            username = foll_user['node']['username']
            user_url = f'https://instagram.com/{username}?__a=1'

            #self.p_users[user]['following'][username].append(foll_user)
            self.p_users[user]['following'][username] = foll_user

            yield response.follow(user_url,
                                  callback=self.parse_foll_user,
                                  cb_kwargs={'user_vars': user_vars, 'user': user, 'foll_user': username}
                                  )

            pass


        if data['data']['user']['edge_follow']['page_info']['has_next_page']:
            user_vars.update({'after': data['data']['user']['edge_follow']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars)

            yield response.follow(next_page,
                                  callback=self.parse_following,
                                  cb_kwargs={'user_vars': user_vars, 'user': user}
                                  )
        pass

    def parse_foll_user(self, response, user_vars, user, foll_user):

        data = json.loads(response.body)

        for post in data['graphql']['user']['edge_owner_to_timeline_media']['edges']:

            user_post_vars = deepcopy(self.variables_post_base)
            user_post_vars.update({'shortcode': post['node']['shortcode']})

            posts_link = self.make_graphql_url(user_post_vars, True)
            yield response.follow(posts_link,
                                  callback=self.parse_posts,
                                  cb_kwargs={'user_vars': user_vars, 'user': user,
                                             'user_post_vars': user_post_vars,
                                             'foll_user': foll_user}
                                  )
            pass
        
        print(1)

    def parse_posts(self, response, user_vars, user, foll_user, user_post_vars):
        data = json.loads(response.body)
        posts = data['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
        pass

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"','')

    def make_graphql_url(self, user_vars, post_hash=False):
        if post_hash:
            query_hash = self.query_post_hash
        else:
            query_hash = self.query_hash

        result = '{url}query_hash={hash}&{variables}'.format(
            url=self.graphql_url, hash=query_hash,
            variables=urlencode(user_vars)
        )
        return result
