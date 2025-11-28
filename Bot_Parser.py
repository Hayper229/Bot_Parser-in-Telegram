from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError
import os
import colorama
import argparse
import time
import telebot

# Настройки для Telethon
api_id = API_ID
api_hash = 'API_HASH'
phone = '+Phone_Number'


client = TelegramClient(phone, api_id, api_hash)

lim = int(5900)

async def get_messages(client, channel, limit=lim):
    messages = []
    async for message in client.iter_messages(channel, limit):
        if message.text:
            messages.append(f"<p style='color: green;'>Message: {message.text}<br>Date: {message.date}</p>")
    return messages

async def join_channel(client, channel_link):
    try:
        await client(JoinChannelRequest(channel_link))
        print(f"{colorama.Fore.CYAN}Присоединился к каналу: {channel_link}")
    except Exception as e:
        print(f"Не удалось присоединиться к каналу: {e}")

async def enum_users(client, channel_link):
    users = await client.get_participants(channel_link)
    user_info = []
    for user in users:
        user_info.append(f"<p style='color: green;'>First_name: {user.first_name}, Last_name: {user.last_name}, Username: {user.username}, ID: {user.id}</p>")
    return user_info

async def generate_report(messages, users):
    with open('report.html', 'a') as f:
        f.write("<html><head><style>body { background-color: black; color: darkgreen; font-family: Arial, sans-serif; } h1, h2 { text-align: center; }</style></head><body>")
        f.write("<h1 style='color: green;'>Отчёт о сообщениях и пользователях</h1>")
        f.write("<h2 style='color: green;'>Messages:</h2>")
        f.write("".join(messages))
        f.write("<h2 style='color: green;'>Users:</h2>")
        f.write("".join(users))
        f.write("</body></html>")

async def send_report(client, channel_link, users, messages):
    with open('report.html', 'r') as f:
         safe = f.read().split()
         await client.send_file('@Your_Username', 'report.html',  caption=f'CH: {channel_link} | \nTotal_Users: {len(users)}\nTotal SMS: {len(messages)}_SMS')
         print("Отчёт отправлен пользователю @Your_Username")

async def func():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="ссылка на канал")
    argum = parser.parse_args()
    channel_link = argum.c
    if not channel_link:
        exit()
    await join_channel(client, channel_link)  
    messages = await get_messages(client, channel_link)  
    users = await enum_users(client, channel_link)     
    await generate_report(messages, users)  
    await send_report(client, channel_link, users, messages)
    print("Отчёт сгенерирован и отправлен.")
    os.system('rm report.html')

async def main():
    try:
        await func()
    except FloodWaitError as a:
        print(f'Flood Wait Error: нужно подождать {a.seconds} секунд.')
        time.sleep(a.seconds)
        await main()

with client:
    client.loop.run_until_complete(main())
                                                                                                                                
