import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


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

    response_data = response.json()['response']['link']

    if url != response_data:
        return True
    return False


def get_api_response(token, url):
    check_link_api_url = "https://api.vk.ru/method/utils.checkLink"

    payload = {
        "access_token": token,
        "url": url,
        "v": "5.199"
    }

    response = requests.post(check_link_api_url, params=payload)
    response.raise_for_status()

    return response.json()


def main():
    load_dotenv()

    token = os.getenv("VK_ID_TOKEN", default=None)

    if token is None or not token:
        return print("В программе отсутствует токен.Обратитесь к администратору.")

    user_input = input("Введите ссылку для сокращения: ")

    try:
        answer = is_shorten_link(token, user_input)
        if answer is True:
            clicks = count_clicks(token, user_input)
            print("Количество переходов по ссылке: ", clicks)
        else:
            short_link = shorten_link(token, user_input)
            print("Сокращенная ссылка: ", short_link)

    except KeyError:
        response_data = get_api_response(token, user_input)
        if response_data['error']['error_code'] == 5:
            print("Ошибка авторизации. Проверьте правильность токена.")
        elif response_data['error']['error_code'] == 100:
            print("Вы ввели неверную ссылку. Ошибка: ", response_data['error']['error_msg'])


if __name__ == '__main__':
    main()
