from typing import Any

import requests

from pathlib import Path
from api.schemas import UploadPhoto, Comic


class VkApiException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_wall_upload_server(group_id: int, token: str) -> str:
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.get(url, params)
    vk_api_response = check_vk_api_err_response(response)

    upload_url = vk_api_response['response']['upload_url']

    return upload_url


def upload_photo_to_server(
        upload_url: str,
        file: Path
) -> UploadPhoto:

    files = {
        'photo': (file.name, file.read_bytes())
    }

    response = requests.post(upload_url, files=files)
    vk_api_response = check_vk_api_err_response(response)

    return UploadPhoto(
        vk_api_response['server'],
        vk_api_response['photo'],
        vk_api_response['hash']
    )


def save_wall_photo(
        group_id: int,
        token: str,
        upload_photo: UploadPhoto
) -> tuple[int, int]:
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    data = {
        'group_id': group_id,
        'server': upload_photo.server_id,
        'photo': upload_photo.photo,
        'hash': upload_photo.hash_upload,
        'access_token': token,
        'v': '5.131'
    }

    response = requests.post(url, data=data)
    vk_api_response = check_vk_api_err_response(response)

    media_id = vk_api_response['response'][0]['id']
    owner_id = vk_api_response['response'][0]['owner_id']

    return media_id, owner_id


def post_on_wall(
        owner_id: int,
        group_id: int,
        photo_id: int,
        message: str,
        token: str
):
    url = 'https://api.vk.com/method/wall.post'
    attachments = f'photo{owner_id}_{photo_id}'
    data = {
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'message': message,
        'attachments': attachments,
        'access_token': token,
        'v': '5.131'

    }
    response = requests.post(url, data)
    check_vk_api_err_response(response)


def check_vk_api_err_response(response: requests.Response) -> Any:
    response.raise_for_status()
    api_response = response.json()
    if not api_response.get('error'):
        return api_response
    error_msg = api_response['error']['error_msg']
    raise VkApiException(error_msg)


def post_comic_on_group_wall(comic: Comic, vk_group_id: int, vk_token: str):
    photo_upload_url = get_wall_upload_server(vk_group_id, vk_token)
    upload_foto_info = upload_photo_to_server(
        photo_upload_url,
        comic.file_path
    )

    media_id, owner_id = save_wall_photo(
        vk_group_id,
        vk_token,
        upload_foto_info
    )

    post_on_wall(
        owner_id,
        vk_group_id,
        media_id,
        comic.comment,
        vk_token
    )
