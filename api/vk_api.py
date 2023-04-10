import requests


def get_wall_upload_server(group_id: int, token: str) -> str:
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.get(url, params)
    response.raise_for_status()
    vk_api_response = response.json()

    upload_url = vk_api_response['response']['upload_url']

    return upload_url


def upload_photo_to_server(
        upload_url: str,
        file_name: str
) -> tuple[int, str, str]:

    with open(file_name, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        vk_api_response = response.json()

        server = int(vk_api_response['server'])
        photo = vk_api_response['photo']
        hash_str = vk_api_response['hash']

    return server, photo, hash_str


def save_wall_photo(
        group_id: int,
        server: int,
        photo: str,
        hash_str: str,
        token: str
) -> tuple[int, int]:

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    data = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash_str,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.post(url, data=data)
    vk_api_response = response.json()
    media_id = int(vk_api_response['response'][0]['id'])
    owner_id = int(vk_api_response['response'][0]['owner_id'])

    return media_id, owner_id


def wall_post(
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
    response.raise_for_status()
