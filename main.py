import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import random
from urllib.parse import urlparse


def get_image_url_and_authors_comment(comics_number):
    url = 'https://xkcd.com/{}/info.0.json'.format(comics_number)
    response = requests.get(url=url)
    response.raise_for_status()
    response_content = response.json()
    image_url = response_content['img']
    authors_comment = response_content['alt']
    return image_url, authors_comment


def download_pictures(image_url,
                      folder_path):
    os.makedirs(folder_path, exist_ok=True)
    parsed_url = urlparse(image_url)
    filename = parsed_url[2][8:]
    file_path = os.path.join(folder_path, filename)
    response = requests.get(url=image_url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_filename_to_upload(folder_path):
    filename = os.listdir(folder_path)
    return filename


def get_vk_response_contents(vk_access_token,
                             vk_group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': vk_access_token,
              'group_id': vk_group_id,
              'v': 5.21,
              }
    response = requests.get(url, params=params)
    response.raise_for_status()
    vk_response_content = response.json()
    return vk_response_content


def get_vk_upload_url(vk_response_content):
    upload_url = vk_response_content['response']['upload_url']
    return upload_url


def get_uri_data(upload_url,
                 file_path):
    with open(file_path, 'rb') as file:
        url = upload_url
        params = {'group_id': 197154009}
        files = { 'file': file

        }
        response = requests.post(url, files=files, params=params)
        response.raise_for_status()
        uri_data_response = response.json()
        return uri_data_response


def save_picture(vk_access_token,
                 uri_data_response,
                 vk_group_id,
                 user_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    hash = uri_data_response['hash']
    photo = uri_data_response['photo']
    server = uri_data_response['server']
    params = {'user_id': user_id,
              'group_id': vk_group_id,
              'hash': hash,
              'photo': photo,
              'server': server,
              'access_token': vk_access_token,
              'v': 5.21
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response_content = response.json()
    media_id = response_content['response'][0]['id']

    return media_id


def publish_picture(vk_access_token,
                    owner_id,
                    attachments,
                    message):
    url = 'https://api.vk.com/method/wall.post'
    params = {
              'owner_id': -owner_id,

              'message': message,
              'attachments': attachments,
              'access_token': vk_access_token,
              'v': 5.21
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response_content = response.json()
    return response_content


def delete_file(file):
    if os.path.isfile(file):
        os.remove(file)


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = 'group ID'
    user_id = 'user ID'

    folder_name = 'Files'
    folder_path = (Path.cwd() / folder_name)

    random_comics_number = random.randint(1, 2331)
    image_url, authors_comment = get_image_url_and_authors_comment(random_comics_number)

    download_pictures(image_url, folder_path)
    filename = get_filename_to_upload(folder_path)[0]
    file_path = os.path.join(folder_path, filename)

    vk_response_content = get_vk_response_contents(vk_access_token,
                                                   vk_group_id)

    vk_upload_url = get_vk_upload_url(vk_response_content)
    uri_data_response = get_uri_data(vk_upload_url,
                                     file_path)

    media_id = save_picture(vk_access_token,
                            uri_data_response,
                            vk_group_id,
                            user_id)

    attachments = f'photo{user_id}_{media_id}'

    publish_picture(vk_access_token,
                    vk_group_id,
                    attachments,
                    authors_comment)

    delete_file(file_path)


if __name__=='__main__':
    main()

