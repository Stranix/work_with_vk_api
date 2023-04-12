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
        api.vk.post_comic_on_group_wall(comic, vk_group_id, vk_token)

    except api.vk.VkApiException as vk_api_err:
        print(vk_api_err.message)

    except Exception as err:
        print(f'Непредвидимая ошибка {err}, {type(err)}')

    finally:
        if comic and os.path.isfile(comic.file_path):
            os.remove(comic.file_path)


if __name__ == '__main__':
    main()
