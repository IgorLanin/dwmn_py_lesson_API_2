import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(token, link):
    url_api_shorten = "https://api.vk.ru/method/utils.getShortLink"

    payload = {
        "access_token": token,
        "url": link,
        "private": "0",
        "v": "5.199"
    }

    response = requests.post(url_api_shorten, params=payload)
    response.raise_for_status()

    return response.json()


def count_clicks(token, link):
    url_api_clicks = "https://api.vk.ru/method/utils.getLinkStats"

    parsed_url = urlparse(link)

    key_url = parsed_url[2].replace("/", "")

    payload = {
        "access_token": token,
        "key": key_url,
        "interval": "forever",
        "v": "5.199"
    }

    response = requests.post(url_api_clicks, params=payload)
    response.raise_for_status()

    clicks = response.json()['response']['stats'][0]['views']

    return clicks


def is_shorten_link(url):
    parsed = urlparse(url)
    for i in parsed:
        if i == "vk.cc":
            return True
    return False


def main():
    load_dotenv()

    token = os.getenv("VK_ID_TOKEN")
    user_input = input("Введите ссылку для сокращения: ")

    if is_shorten_link(user_input) is True:
        try:
            clicks = count_clicks(token, user_input)
            print("Количество переходов по ссылке: ", clicks)
        except:
            print("Что-то пошло не так. Попробуйте повторить запрос позже.")
    else:
        try:
            short_link = shorten_link(token, user_input)['response']['short_url']
            print("Сокращенная ссылка: ", short_link)
        except:
            if shorten_link(token, user_input)['error']['error_code'] == 5:
                print("Ошибка авторизации. Проверьте правильность токена")
            elif shorten_link(token, user_input)['error']['error_code'] == 100:
                print("Вы ввели неверную ссылку. Ошибка: ", shorten_link(token, user_input)['error']['error_msg'])


if __name__ == '__main__':
    main()
