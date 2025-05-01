import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
            description='''Программа сокращает ссылку через VK API.
            Если передана сокращенная ссылка - возвращает количество переходов''',
            prog='Сокращение ссылок/статистика переходов')

    parser.add_argument(
            'link',
            help='Ссылка для сокращения или отображения кол-ва переходов.')

    return parser


def shorten_link(token, link):
    shorten_api_url = "https://api.vk.ru/method/utils.getShortLink"

    payload = {
        "access_token": token,
        "url": link,
        "private": "0",
        "v": "5.199"
    }

    response = requests.post(shorten_api_url, params=payload)
    response.raise_for_status()

    short_link = response.json()['response']['short_url']

    return short_link


def count_clicks(token, link):
    count_clicks_api_url = "https://api.vk.ru/method/utils.getLinkStats"

    parsed_url = urlparse(link)

    short_url_key = parsed_url[2].replace("/", "")

    payload = {
        "access_token": token,
        "key": short_url_key,
        "interval": "forever",
        "v": "5.199"
    }

    response = requests.post(count_clicks_api_url, params=payload)
    response.raise_for_status()

    clicks = response.json()['response']['stats'][0]['views']

    return clicks


def is_shorten_link(token, url):
    check_link_api_url = "https://api.vk.ru/method/utils.checkLink"

    payload = {
        "access_token": token,
        "url": url,
        "v": "5.199"
    }

    response = requests.post(check_link_api_url, params=payload)
    response.raise_for_status()

    responding_data = response.json()

    if "error" in responding_data:
        raise Exception(f"Ошибка при выполнении запроса: {responding_data['error']['error_msg']}")

    return url != responding_data['response']['link']


def main():
    load_dotenv()

    token = os.getenv("VK_ID_TOKEN", default=None)

    if token is None or not token:
        return print("В программе отсутствует токен. Обратитесь к администратору.")

    parser = create_parser()
    user_input = parser.parse_args()

    try:
        if is_shorten_link(token, user_input.link):
            clicks = count_clicks(token, user_input.link)
            print("Количество переходов по ссылке: ", clicks)
        else:
            short_link = shorten_link(token, user_input.link)
            print("Сокращенная ссылка: ", short_link)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
