from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm
import asyncio

api_id = 14992732   # Your API ID
api_hash = 'bca56746c7e90065b3c7e8071850997f'  # Your API HASH


def download_media(group, cl, name):
    messages = cl.get_messages(group, limit=1)

    for message in tqdm(messages):
        message.download_media('./' + name + '/')

def main():
    api_id = 14992732  # Your API ID
    api_hash = 'bca56746c7e90065b3c7e8071850997f'  # Your API HASH

    with TelegramClient('name', api_id, api_hash) as client:
        result = client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=500,
            hash=0,
        ))

        title = 'Birinci Kanal'            # Title for group chat
        for chat in result.chats:
            print(chat)

            if chat.title == title:
                download_media(chat, client, title)
main()