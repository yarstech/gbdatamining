import requests
from bs4 import BeautifulSoup
import time
import json

domain_url = 'https://geekbrains.ru'
blog_url = 'https://geekbrains.ru/posts'


def get_page_strict(soup):
    posts_list = []
    posts_data = soup.find_all('div', class_='post-item')

    for post in posts_data:

        post_url = f"{domain_url}{post.find('a').attrs.get('href')}"

        #обращаемся к странице статьи и парсим непосредственно ее
        post_data = requests.get(post_url)
        soup_post_data = BeautifulSoup(post_data.text, 'lxml')

        #парсим страницу
        title = soup_post_data.find('div', class_='blogpost-description').find('span').text
        pub_date = soup_post_data.find('div', class_='blogpost-date-views').find('time').attrs.get("datetime")

        content = soup_post_data.find('div', class_='blogpost-content')

        try:
            image = content.find('img').attrs.get('src')
        except AttributeError as e:
            image = ''
            pass

        #текст вытащим без тэгов
        text = ''
        for i in range(1, len(content.contents)):
            if not content.contents[i].find('text') == -1:
                text = text + '\n' + content.contents[i].text

        author_name = soup_post_data.find('div', class_='row m-t').find('a').find('div', class_='text-lg').text
        author_url = f"{domain_url}{soup_post_data.find('div', class_='row m-t').find('a').attrs.get('href')}"

        author = {
            'name': author_name,
            'url': author_url
        }

        post_dict = {
            'post_url': post_url,
            'post_title': post.find(class_='post-item__title').text,
            'post_date': post.find(class_='small m-t-xs').text,
            'title': title,
            'image': image,
            'text': text,
            'pub_date': pub_date,
            'author': author
        }

        posts_list.append(post_dict)

    return posts_list

def get_page_soup(url):
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data

def parser(url):
    posts_list = []

    while True:
        soup = get_page_soup(url)
        posts_list.extend(get_page_strict(soup))

        #break - для отладки на примере одной страницы

        try:
            url = soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')

        except AttributeError as e:
            break

        url = f"{domain_url}{url}"
        time.sleep(1)

    return posts_list

result_data = parser(blog_url)

with open('gb_blog.json', 'w') as j_file:
    j_file.write(json.dumps(result_data))

pass