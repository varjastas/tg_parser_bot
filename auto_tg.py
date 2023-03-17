import asyncio
import os
import json
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.messages import SendReactionRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest

api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
client = TelegramClient(
    'denizzzka2125',
    api_id,
    api_hash,
    )
with open('channels.json') as channels:
    channels = json.load(channels)
ban_words = ['mvp', 'funko', 'trader', 'pnl', 'bot', '1 day', 'Bybit Spot', 'softers', 'Bybit Quest', 'Margin', 'Grid Bot', 'Perpetual Contract', 'Bybit CEO', 'Deposit', 'Bybit Savings', 'vip', 'delisting', 'wallet', 'top traders', 'copy', 'trading']
channel = 'kljhjdfghoi6e4sdgsd54gf'


# Choice the action
async def choice_action():
    change_true = True
    while change_true:
        action = input('What do you want to do?\n'
                    'Change profile info - 1\n'
                    'Add private channel - 2\n'
                    'Add public channel - 3\n'
                    'Check my channels - 4\n'
                    'Send reaction - 5\n'
                    'Exit (start parsing) - 6\n')
        match action:
            case '1':
                await change_profile()
            case '5':
                await send_reaction()
            case '3':
                await add_public_channel()
            case '2':
                await add_private_channel()
            case '4':
                check_channels()
            case '6':
                change_true = False
            case _:
                print('Wrong choice')



@client.on(events.NewMessage)
async def handler(event):
    count = 0
    message = event.message.to_dict()['message']
    entities = event.message.to_dict()['entities']
    if event.peer_id.channel_id in channels.values():
        for i in range(len(ban_words)):
            if ban_words[i].lower() not in message.lower():
                count += 1
            if count == len(ban_words):
                ch_full = await client(GetFullChannelRequest(channel=event.peer_id.channel_id))
                if ch_full.to_dict()['chats'][0]['noforwards']:
                    for key, value in channels.items():
                                if value == event.peer_id.channel_id:
                                    key = key.replace(' ', '_')
                                    if len(entities) > 0:
                                        for i in range(len(entities)):
                                            if entities[i]['_'] == 'MessageEntityTextUrl':
                                                url = entities[i]['url']
                                                if 't.me' not in url:
                                                    message += f'\n\n{url}'
                                        message += f'\n\n**#{key}**'
                    if event.message.to_dict()['media'] is not None:
                        file_ms = await client.download_media(message=event.message)
                        await client.send_message(channel, message, file=file_ms)
                        os.remove(file_ms)
                        await asyncio.sleep(1)
                    else:
                        await client.send_message(channel, message)
                else:
                    await client.forward_messages(channel, event.message)


def check_channels():
    print(*channels.keys(), sep='\n', end='\n\n')


# Full info
async def change_profile():
    change_true = True
    while change_true:
        me = await client.get_me()
        bio = await client(GetFullUserRequest(me.username))
        bio = bio.full_user.about
        print(f'INFO | Phone: {me.phone} | Username: {me.username} | Fname: {me.first_name} | Lname: {me.last_name} | Bio: {bio} | Photoid: {me.photo.photo_id}')
        action = input('What do you want to change?\n'
                    'bio - 1\n'
                    'name - 2\n'
                    'photo - 3\n'
                    'username - 4\n'
                    'exit - 5\n')
        match action:
            case '1':
                await change_bio()
            case '2':
                await change_name()
            case '3':
                await change_photo()
            case '4':
                await change_username()
            case '5':
                change_true = False
            case _:
                print('Wrong choice')


# Change name
async def change_name():
    new_fname = input('Enter new first name:\n')
    new_lname = input('Enter new last name:\n')
    await client(UpdateProfileRequest(last_name=new_lname, first_name=new_fname))
    print('--> Done\n')


# Change bio
async def change_bio():
    new_bio = input('Enter new bio:\n')
    await client(UpdateProfileRequest(about=new_bio))
    print('--> Done\n')


# Change username
async def change_username():
    new_username = input('Enter new username:\n')
    await client(UpdateUsernameRequest(new_username))
    print('--> Done\n')


# Change photo
async def change_photo():
    new_photo = input(r'Enter the address of the photo, for example: "C:\Users\me\photo.png"'+'\n')
    await client(UploadProfilePhotoRequest(await client.upload_file(new_photo)))
    print('--> Done\n')


# Send reaction
async def send_reaction():
    channel = input('Enter the channel username:\n')
    chat = await client(GetFullChannelRequest(channel))
    emoji = {key+1: chat.full_chat.available_reactions[key] for key in range(len(chat.full_chat.available_reactions))}
    choice_react = ''
    for i in emoji:
        choice_react += emoji[i] + ' - ' + str(i) + '\n'
    react = int(input(f'Choose emoji:\n{choice_react.strip()}\n'))
    reaction = emoji[react]
    last_message = await client.get_messages(channel, limit=1)
    print(f'Ð<9f>Ð¾Ñ<81>Ð»ÐµÐ´Ð½ÐµÐµ Ñ<81>Ð¾Ð¾Ð±Ñ<89>ÐµÐ½Ð¸Ðµ: {last_message[0].id}')
    msg_id = int(input('Enter message id: '))
    result = await client(SendReactionRequest(
             peer=channel,
             msg_id=msg_id,
             reaction=reaction
             ))
    print(f'--> Done | {str(result.date)[0:-6]}\n')


# Add private channel
async def add_private_channel():
    link = input('Enter link like "xVOb2354y6XgsdzMzxczy":\n')
    info = await client(ImportChatInviteRequest(link))
    channels[info.chats[0].title] = info.chats[0].id
    with open('channels.json', 'w') as outfile:
        json.dump(channels, outfile)
    print('--> Done\n')


# Add public channel
async def add_public_channel():
    link = input('Enter channel username like "pirblog":\n')
    info = await client(JoinChannelRequest(link))
    channels[info.chats[0].title] = info.chats[0].id
    with open('channels.json', 'w') as outfile:
        json.dump(channels, outfile)
    print('--> Done\n')


async def main():
    await choice_action()


if __name__ == '__main__':
    try:
        with client:
            client.loop.run_until_complete(main())
            client.run_until_disconnected()
    except Exception as ex:
        print(ex)