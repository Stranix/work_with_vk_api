import os
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
    with open(f'../{path_to_save}/{image_name}', 'wb') as image_file:
        image_file.write(response.content)


def remove_file(file_name: str):
    if os.path.isfile(file_name):
        os.remove(file_name)
        return
    print(f'Ошибка: файл {file_name} не найден')
