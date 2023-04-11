import requests
import random

from pathlib import Path
from api.schemas import Comic


def get_comic(number: int) -> Comic:
    url = f'https://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    comic_comment = comic['alt']
    image_url = comic['img']
    image_name = 'comics_{}.png'.format(number)

    return Comic(image_url, image_name, Path(image_name), comic_comment)


def get_random_comic_num() -> int:
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_count = response.json()['num']
    random_comic_num = random.randint(1, comics_count)

    return random_comic_num


def download_comic(comic: Comic) -> bool:
    response = requests.get(comic.image_url)
    response.raise_for_status()
    comic.file_path.write_bytes(response.content)
    return True
