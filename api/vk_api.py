import requests

from pathlib import Path
from api.schemas import UploadPhoto


class TokenExpiredException(Exception):
    pass


def get_wall_upload_server(group_id: int, token: str) -> str:
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.get(url, params)
    vk_api_check_err_response(response)
    vk_api_response = response.json()
    upload_url = vk_api_response['response']['upload_url']

    return upload_url


def upload_photo_to_server(
        upload_url: str,
        file: Path
) -> UploadPhoto:
    files = {
        'photo': file.read_bytes()
    }
    response = requests.post(upload_url, files=files)
    vk_api_check_err_response(response)
    vk_api_response = response.json()

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
        'hash': upload_photo.hash,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.post(url, data=data)
    vk_api_check_err_response(response)
    vk_api_response = response.json()
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
    vk_api_check_err_response(response)


def vk_api_check_err_response(response: requests.Response) -> bool:
    response.raise_for_status()
    if response.json()['error']:
        raise TokenExpiredException
    return True
