import re
import requests
import json
import os

from bs4 import BeautifulSoup as bs


def download_post(post_id):
    link = f'https://habr.com/ru/post/{post_id}/'
    page = requests.get(link)
    soup = bs(page.text, 'html.parser')

    title = soup.find('meta', property='og:title')
    title = str(title).split('="')[1].split('" ')[0]

    post = str(soup.find('div', id="post-content-body"))
    post = post.strip()
    post = post.split('id="post-content-body">')[1].split('</div>')[0]
    post = re.sub(r'<[^>]*>', '', post)
    return {'title': title, 'text': post}


def get_article(category_link):
    page = requests.get(category_link)
    data = page.text
    all_articles = re.findall(r'ru/post/\d{3,}', data)
    all_articles = list(set(all_articles))
    posts_id = [x.replace('ru/post/', '') for x in all_articles]
    return posts_id


if __name__ == '__main__':
    categories = ['infosecurity', 'electronics', 'hi', 'controllers', 'machine_learning',
                  'bigdata', 'analysis_design', 'crypto', 'natural_language_processing',
                  'compilers', 'data_mining', 'industrial_control_system', 'oop']

    path_to_save = 'H:\\Diplom_Dataset\\'

    for category in categories:
        for page in range(2, 200):
            category_link = f'https://habr.com/ru/hub/{category}/page{page}/'
            article = get_article(category_link)
            if len(article) == 0:
                print(f'Закончил поиск в категории {category} на {page} странице')
                break
            for art_id in article:
                try:
                    filename = os.path.join(path_to_save, art_id) + '.json'
                    post = download_post(art_id)
                    with open(filename, 'w', encoding='utf-8') as json_file:
                        json.dump(post, json_file, ensure_ascii=False)
                except Exception as E:
                    print(E)
