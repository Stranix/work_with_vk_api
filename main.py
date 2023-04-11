import os
import api

from dotenv import load_dotenv


def main():
    try:
        load_dotenv()
        vk_token = os.environ['VK_ACCESS_TOKEN']
        vk_group_id = int(os.environ['VK_GROUP_ID'])

        random_comic_num = api.comics.get_random_comic_num()
        comic = api.comics.get_comic(random_comic_num)
        if not api.comics.download_comic(comic):
            os.remove(comic.file_path)
            raise ValueError

        photo_upload_url = api.vk.get_wall_upload_server(vk_group_id, vk_token)

        upload_foto_info = api.vk.upload_photo_to_server(
            photo_upload_url,
            comic.file_path
        )

        media_id, owner_id = api.vk.save_wall_photo(
            vk_group_id,
            vk_token,
            upload_foto_info
        )

        api.vk.post_on_wall(
            owner_id,
            vk_group_id,
            media_id,
            comic.comment,
            vk_token
        )

        os.remove(comic.file_path)
    except Exception as err:
        print(f'Непредвидимая ошибка {err}, {type(err)}')


if __name__ == '__main__':
    main()
