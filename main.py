import argparse
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

BITLY_GENERIC_ACCESS_TOKEN = os.getenv('BITLY_GENERIC_ACCESS_TOKEN')
URL_TEMPLATE = 'https://api-ssl.bitly.com/v4/{}'


def shorten_link(BITLY_GENERIC_ACCESS_TOKEN, link):

    shorten_link_url = URL_TEMPLATE.format('shorten')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(BITLY_GENERIC_ACCESS_TOKEN)
    }

    body = {
        "domain": "bit.ly",
        "long_url": link
    }

    response = requests.post(shorten_link_url, headers=headers, json=body)

    if response.ok:
        bitlink = response.json()['link']
        return bitlink
    else:
        raise requests.HTTPError(response.text)


def cut_link_protocol(link):
    link_without_protocol = re.sub(r'(^.*//)', '', link)
    return link_without_protocol


def count_clicks(BITLY_GENERIC_ACCESS_TOKEN, bitlink):
    bitlink_without_protocol = cut_link_protocol(bitlink)
    summary_clicks_url = URL_TEMPLATE.format('bitlinks/{}/clicks/summary'
                                        .format(bitlink_without_protocol))

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(BITLY_GENERIC_ACCESS_TOKEN)
    }

    body = {
        "units": -1,
        "unit": "day"
    }

    response = requests.get(summary_clicks_url, headers=headers, json=body)

    if response.ok:
        clicks_count = response.json()['total_clicks']
        return clicks_count
    else:
        raise requests.HTTPError(response.text)


def print_shorten_link(BITLY_GENERIC_ACCESS_TOKEN, link):
    try:
        bitlink = shorten_link(BITLY_GENERIC_ACCESS_TOKEN, link)
    except requests.exceptions.HTTPError as error:
        return print('Возникла ошибка получения короткой ссылки: \n{}.'.format(error))
    return print(bitlink)


def print_clicks_count(BITLY_GENERIC_ACCESS_TOKEN, bitlink):
    try:
        clicks_count = count_clicks(BITLY_GENERIC_ACCESS_TOKEN, bitlink)
    except requests.exceptions.HTTPError as error:
        return print('Возникла ошибка подсчёта переходов по ссылке: \n{}.'.format(error))
    return print('Количество переходов по ссылке: {}'.format(clicks_count))


def is_bitlink(BITLY_GENERIC_ACCESS_TOKEN, link):

    bitlink_without_protocol = cut_link_protocol(link)
    retrieve_bitlink_url = URL_TEMPLATE.format('/bitlinks/{}'.format(bitlink_without_protocol))

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(BITLY_GENERIC_ACCESS_TOKEN)
    }

    response = requests.get(retrieve_bitlink_url, headers=headers)
    return response.ok


def create_parser():
    parser = argparse.ArgumentParser(description='''Скрипт сокращает ссылку при помощи сервиса bit.ly 
                                                    или выводит количество переходов по ней, если была 
                                                    введена уже сокращенная ссылка.''')
    parser.add_argument('link',
                        help='''Ссылка для сокращения или получения количества переходов 
                                по уже сокращенной ссылке.''', 
                        nargs='?')
 
    return parser


def main():

    parser = create_parser()
    args = parser.parse_args()

    if args.link:

        link = args.link

        if is_bitlink(BITLY_GENERIC_ACCESS_TOKEN, link):
            print_clicks_count(BITLY_GENERIC_ACCESS_TOKEN, link)
        else:
            print_shorten_link(BITLY_GENERIC_ACCESS_TOKEN, link)

    else:
        exit("Не указана ссылка!")


if __name__ == '__main__':
    main()
