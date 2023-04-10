import os
import services

from dotenv import load_dotenv


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = int(os.getenv('VK_GROUP_ID'))

    services.create_comics_post_on_vk_group(vk_group_id, vk_token)


if __name__ == '__main__':
    main()
