import requests
import services

from typing import Any


def get_comics(number: int) -> tuple[Any, str]:
    url = f'https://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    comics_commit = comics['alt']
    image_url = comics['img']
    image_name = 'comics_{}.png'.format(number)
    services.download_image(image_url, './', image_name)
    return comics_commit, image_name


def get_comics_count() -> int:
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_count = response.json()['num']

    return comics_count
