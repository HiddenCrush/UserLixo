from pyrogram import Client, Filters
from config import git_repo
import subprocess
from db import db, save
import sys
import os
import time
import threading

@Client.on_message(Filters.command("upgrade", prefixes="!"))
def uprade(client, message):
    a = client.send_message('me', 'Atualizando...')
    out = subprocess.getstatusoutput('git pull {}'.format(' '.join(git_repo)))[1]
    a.edit(f'Resultado da atualização:\n{out}')
    sent = message.edit('Reiniciando...')
    db["restart"] = {'cid':message.chat.id, 'mid':sent.message_id}
    save(db)
    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)
    del threading.Thread