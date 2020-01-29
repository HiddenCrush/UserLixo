from pyrogram import Client, Filters
import math
from PIL import Image
import time
import urllib.request
from time import sleep
import os

@Client.on_message(Filters.command("kibe", prefixes = '.') & Filters.me)
def kibe(client,message):
    emoji = message.text[6:]
    rsize = False
    ctime = time.time()
    user = client.get_me()
    if not user.username:
        user.username = user.first_name
    packname = f"a{user.id}_by_{user.username}_amn"
    packnick = f"@{user.username}'s kibe pack"
    rmessage = message.reply_to_message
    if rmessage and rmessage.media:
        if rmessage.photo:
            photo = client.download_media(rmessage.photo.file_id, rmessage.photo.file_ref,file_name=f'./{ctime}.png')
            rsize = True
        if rmessage.document:
            photo = client.download_media(rmessage.document.file_id, rmessage.document.file_ref,file_name=f'./{ctime}.png')
            rsize = True
        elif rmessage.sticker:
            if len(emoji) == 0:
                emoji = rmessage.sticker.emoji
            if rmessage.sticker.is_animated:
                photo = client.download_media(rmessage.sticker.file_id, rmessage.sticker.file_ref,file_name=f'./{ctime}.tgs')
                packname += '_animated'
                packnick += ' animated'
            else:
                photo = client.download_media(rmessage.sticker.file_id, rmessage.sticker.file_ref,file_name=f'./{ctime}.webp')
                rsize = True
        if rsize:
            photo = resize_photo(photo,ctime)
        print(f'packname: "{packname}", packnick: "{packnick}')
        response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')
        st = 'Stickers'
        if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
            client.send_message(st, '/addsticker')
            sleep(0.3)
            client.send_message(st, packname)
            print(photo)
            client.send_document(st, photo)
            sleep(0.3)
            client.send_message(st, emoji)
            sleep(0.3)
            client.send_message(st, '/done')
            message.edit(f'[kibed](http://t.me/addstickers/{packname})')
        else:
            message.edit('criando novo pack')
            client.send_message(st, '/newpack')
            sleep(0.3)
            client.send_message(st, packnick)
            sleep(0.3)
            client.send_document(st, photo)
            sleep(0.3)
            client.send_message(st, emoji)
            sleep(0.5)
            client.send_message(st, '/publish')
            sleep(0.3)
            client.send_message(st, '/skip')
            sleep(0.3)
            client.send_message(st, packname)
            message.edit(f'[kibed](http://t.me/addstickers/{packname})')
        os.remove(photo)
            
def resize_photo(photo, ctime):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)
    os.remove(photo)
    image.save(f'./{ctime}.png')

    return f'./{ctime}.png'

