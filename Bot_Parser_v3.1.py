from telethon import TelegramClient, events, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import UserStatusOnline
import os
import colorama
import argparse
import asyncio
import time

colorama.init(autoreset=True)

# Данные авторизации
api_id = API_ID
api_hash = 'API_HASH'
phone = 'PHONUMBER'
ADMIN_TAG = '@Username'

client = TelegramClient(phone, api_id, api_hash)


@client.on(events.NewMessage)
async def live_monitor(event):
    if event.message.text:
        logs_log = []
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.GREEN}LIVE{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.MAGENTA}{event.chat_id}]{colorama.Fore.YELLOW}: {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{event.message.text[:50]}")
        log = f'[{time.asctime()}] ID: {event.chat_id}| Msg: {event.message.text[:50]}'
        with open('message.log', 'a') as f:
             f.write(f'{log}\n')
        with open('message.log', 'r') as f:
             logged = f.readlines()
             print(f'{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Logged messages{colorama.Fore.YELLOW}...{colorama.Fore.YELLOW}{len(logged)}')
             logged.clear()
        

async def track_status(user_handle):
    last_status = None
    print(f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}*{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Трекер статуса для {colorama.Fore.YELLOW}{user_handle} {colorama.Fore.GREEN}запущен.")
    while True:
        try:
            full = await client(GetFullUserRequest(user_handle))
            is_online = isinstance(full.user.status, UserStatusOnline)
            if is_online != last_status:
                status_text = "В СЕТИ 🟢" if is_online else "ВЫШЕЛ 🔴"
                await client.send_message(ADMIN_TAG, f"👤 СТАТУС: {user_handle} теперь {status_text}")
                last_status = is_online
        except Exception:
            pass
        await asyncio.sleep(30)


async def get_messages(client, channel, limit=3900):
    messages = []
    try:
        entity = await client.get_entity(channel)
        print(f"{colorama.Fore.YELLOW}[+] Цель: {entity.title}. Начинаю сбор сообщений...")
        async for message in client.iter_messages(entity, limit):
            if message.text:
                user_id = message.from_id if message.from_id else 'Unknown'
                print(f'{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{message.text} {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{user_id}{colorama.Fore.WHITE}][{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.MAGENTA}{message.date}{colorama.Fore.WHITE}]{colorama.Fore.RESET}')
                messages.append(f"<p style='color: green;'>Message: {message.text}<br>ID: {user_id}<br>Date: {message.date}</p><hr>\n")

        return messages
    except Exception as e:
        print(f"{colorama.Fore.RED}Ошибка при сборе сообщений: {e}")
        return []

async def enum_users(client, channel_link):
    try:
        users = await client.get_participants(channel_link)
        return [f"<p style='color: green;'>First_name: {u.first_name}, Last_name: {u.last_name}, Username: {u.username}, ID: {u.id}</p>" for u in users]
    except Exception as e:
        print(f"{colorama.Fore.RED}Ошибка при парсинге участников: {e}")
        return []

async def generate_report(messages, users):
    with open('report.html', 'a', encoding='utf-8') as f:
        f.write("<html><body style='background-color: black; color: darkgreen; font-family: Arial;'>")
        f.write(f"\n<h3 style='color: green;'>Generated on <span style='color: red;'>{time.asctime()}</span></h3>\n") # New function
        f.write(f"\n<h2 style='color: green;'>Total messages: <span style='color: yellow;'>{len(messages)}</span></h2>\n")
        f.write("".join(messages))
        f.write(f"\n<h2 style='color: green;'>Total users: <span style='color: yellow;'>{len(users)}</span></h2>\n")
        f.write("".join(users) + "</body></html>")

async def func():
 try:
    os.remove('message.log')
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="ссылка на канал")
    parser.add_argument("-u", help="юзернейм для слежки за статусом")
    argum = parser.parse_args() 
    if argum.u:
       asyncio.create_task(track_status(argum.u))
       pass
    if not argum.c:
       print(f"{colorama.Fore.YELLOW}Укажите канал (-c) или цель (-u). Бот переходит в LIVE режим.")
       return
    print(f"{colorama.Fore.YELLOW}[*] Начинаю сбор данных из {argum.c}...")
    messages = await get_messages(client, argum.c)
    users = await enum_users(client, argum.c)
    await generate_report(messages, users)
    await client.send_file(ADMIN_TAG, 'report.html', caption=f'CH: {argum.c} | \nTotal Users: {len(users)}\nTotal Messages: {len(messages)}\nDate: {time.asctime()}')
    print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Отчет отправлен {colorama.Fore.YELLOW}{ADMIN_TAG}\n{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total users {colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(users)}\n{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total messages {colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(messages)}")
    os.remove('report.html')
 except:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="ссылка на канал")
    parser.add_argument("-u", help="юзернейм для слежки за статусом")
    argum = parser.parse_args() 
    if argum.u:
       asyncio.create_task(track_status(argum.u))
       pass
    if not argum.c:
       print(f"{colorama.Fore.YELLOW}Укажите канал (-c) или цель (-u). Бот переходит в LIVE режим.")
       return
    print(f"{colorama.Fore.YELLOW}[*] Начинаю сбор данных из {argum.c}...")
    messages = await get_messages(client, argum.c)
    users = await enum_users(client, argum.c)
    await generate_report(messages, users)  
    await client.send_file(ADMIN_TAG, 'report.html', caption=f'CH: {argum.c} | \nTotal Users: {len(users)}\nTotal Messages: {len(messages)}\nDate: {time.asctime()}')
    print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Отчет отправлен {ADMIN_TAG}\n{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total users {colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(users)}\n{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total messages {colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(messages)}")
    os.remove('report.html')


async def main():
    try:
        await func()
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.CYAN}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.CYAN}LIVE{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] Мониторинг запущен. Ctrl+C для выхода.")
        await client.run_until_disconnected()
    except errors.FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        await main()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
