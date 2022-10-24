import vk_api
import os
import time
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from toks import group_token, admin_id, group_id, admin_login, admin_password
from vk_api.utils import get_random_id


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device



# vk_session = vk_api.VkApi(token = group_token)
# vk = vk_session.get_api()
#
# session = vk.AuthSession(scope='wall', user_login=admin_login, user_password=admin_password)
# api = vk.API(session, v="5.92")

def change_group_profile_pic(vk, picture, request):

    server = request['server']
    hash = request['hash']

    vk.photos.saveOwnerPhoto(server=server, hash=hash, photo=picture)

    posts = vk.wall.get(owner_id=-group_id)
    post_id = posts["items"][0]["id"]
    vk.wall.delete(owner_id=-group_id, post_id=post_id)

    photos = vk.photos.getAll(owner_id=-group_id)
    if (photos['count'] > 1):
        photo_id = photos["items"][1]["id"]
        vk.photos.delete(owner_id=-group_id, photo_id=photo_id)



# vk.messages.send(
#         peer_id = admin_id,
#         random_id = get_random_id(),
#         message='111'
# )





def main():

    vk_session = vk_api.VkApi(admin_login, admin_password, auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()


    i = 0
    images = os.listdir("logos")
    url = vk.photos.getOwnerPhotoUploadServer(owner_id=-group_id)['upload_url']
    photo = []
    for image in images:
        request = requests.post(url, files={'photo': open('logos/' + image, 'rb')}).json()
        photo.append(request['photo'])
    server = request['server']
    hash = request['hash']

    while True:
        change_group_profile_pic(vk, photo[i], request)
        i = (i+1)%len(photo)
        time.sleep(60*30)





if __name__ == '__main__':
    main()