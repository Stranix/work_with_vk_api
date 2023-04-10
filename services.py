import os
import api
import random
import requests

from pathlib import Path


def download_image(
        image_url: str,
        path_to_save: str,
        image_name: str,
        params=None
):
    response = requests.get(image_url, params=params)
    response.raise_for_status()

    Path(path_to_save).mkdir(exist_ok=True, parents=True)
    with open(f'./{path_to_save}/{image_name}', 'wb') as image_file:
        image_file.write(response.content)


def create_comics_post_on_vk_group(vk_group_id: int, vk_token: str):

    comics_count = api.comics.get_comics_count()
    comics_random_num = random.randint(1, comics_count)

    comics_message, file_name = api.comics.get_comics(comics_random_num)

    photo_upload_url = api.vk.get_wall_upload_server(
        vk_group_id,
        vk_token
    )

    server, photo, hash_str = api.vk.upload_photo_to_server(
        photo_upload_url,
        file_name
    )

    media_id, owner_id = api.vk.save_wall_photo(
        vk_group_id,
        server,
        photo,
        hash_str,
        vk_token
    )

    api.vk.wall_post(
        owner_id,
        vk_group_id,
        media_id,
        comics_message,
        vk_token
    )

    remove_file(file_name)


def remove_file(file_name: str):
    if os.path.isfile(file_name):
        os.remove(file_name)
        return
    print(f'Ошибка: файл {file_name} не найден')
