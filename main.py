import os
import random

import services
from dotenv import load_dotenv

from api.comics_api import get_comics, get_comics_count
from api.vk_api import get_wall_upload_server, upload_photo_to_server, \
    save_wall_photo, wall_post


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = int(os.getenv('VK_GROUP_ID'))

    comics_random_num = random.randint(1, get_comics_count())
    comics_message, file_name = get_comics(comics_random_num)

    photo_upload_url = get_wall_upload_server(vk_group_id, vk_token)
    server, photo, hash_str = upload_photo_to_server(
        photo_upload_url,
        file_name
    )

    media_id, owner_id = save_wall_photo(
        vk_group_id,
        server,
        photo,
        hash_str,
        vk_token
    )

    wall_post(owner_id, vk_group_id, 1, media_id, comics_message, vk_token)
    services.remove_file(file_name)


if __name__ == '__main__':
    main()
