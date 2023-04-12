import os
import api

from dotenv import load_dotenv


def main():
    comic = ''
    try:
        load_dotenv()
        vk_token = os.environ['VK_ACCESS_TOKEN']
        vk_group_id = int(os.environ['VK_GROUP_ID'])

        random_comic_num = api.comics.get_random_comic_num()
        comic = api.comics.get_comic(random_comic_num)
        api.comics.download_comic(comic)

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

    except api.vk.TokenExpiredException:
        print('Истек срок действия токена. Необходимо обновить')

    except Exception as err:
        print(f'Непредвидимая ошибка {err}, {type(err)}')

    finally:
        if comic and os.path.isfile(comic.file_path):
            os.remove(comic.file_path)


if __name__ == '__main__':
    main()
