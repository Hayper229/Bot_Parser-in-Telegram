from telethon import TelegramClient, events, errors, connection
from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import UserStatusOnline, Channel, PeerUser, PeerChannel
import os
import colorama
import argparse
import asyncio
import time
from datetime import datetime, timezone

colorama.init(autoreset=True)

api_id = API_ID
api_hash = 'API_HASH'
phone = '+PHONUMBER'
ADMIN_TAG = '@Your_Username'

PROXY_LIST = [
    ('IP', PORT, 'SECRET'),
    ('IP', PORT, 'SECRET'),
    ('IP', PORT, 'SECRET'),
]

client = None
live_start_time = None

async def init_client():
    global client
    for p_host, p_port, p_secret in PROXY_LIST:
        print(f"{colorama.Fore.CYAN}[*] Пробую подключение через прокси: {p_host}:{p_port}")
        try:
            proxy = (p_host, p_port, p_secret)
            cl = TelegramClient(phone, api_id, api_hash, 
                                proxy=proxy, 
                                connection=connection.ConnectionTcpMTProxyIntermediate,
                                connection_retries=1, 
                                retry_delay=1)
            await cl.connect()
            if cl.is_connected():
                print(f"{colorama.Fore.GREEN}[+] Успешное соединение через {p_host}")
                client = cl
                return
            await cl.disconnect()
        except Exception: continue
    print(f"{colorama.Fore.RED}[!] Рабочих прокси нет. Пробую напрямую...")
    client = TelegramClient(phone, api_id, api_hash)
    await client.connect()

async def smart_join(target):
    try:
        if 't.me/joinchat/' in target or 't.me/+' in target:
            hash_code = target.split('/')[-1].replace('+', '')
            await client(ImportChatInviteRequest(hash_code))
        else:
            entity = await client.get_entity(target)
            await client(JoinChannelRequest(entity))
    except Exception: pass

def format_user_id(peer):
    """Форматирует ID для вывода в терминале без дублей"""
    if isinstance(peer, PeerUser):
        return f"PeerUser(user_id={peer.user_id})"
    elif isinstance(peer, PeerChannel):
        return f"PeerChannel(channel_id={peer.channel_id})"
    return str(peer)

async def get_messages(channel_link, limit=3900):
    all_data = {"main": None, "linked": None, "msgs": []}
    try:
        await smart_join(channel_link)
        main_entity = await client.get_entity(channel_link)
        all_data["main"] = main_entity
        is_channel = isinstance(main_entity, Channel) and not main_entity.megagroup

        def get_time():
            return f"{colorama.Fore.WHITE}[{colorama.Fore.BLUE}{time.asctime()}{colorama.Fore.WHITE}]"

        if is_channel:
            async for m in client.iter_messages(main_entity, limit=100):
                if m.text:
                    u_id_str = format_user_id(m.from_id) if m.from_id else "ChannelPost"
                    print(f"{get_time()}{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{m.text[:40]} {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{u_id_str}{colorama.Fore.WHITE}] [{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.MAGENTA}{m.date}{colorama.Fore.WHITE}]")
                    all_data["msgs"].append(f"<p><span style='color: #00FF00;'>[</span><span style='color: #da70d6;'>CHANNEL</span><span style='color: #00FF00;'>]</span> <span style='color: #00FF00;'>Message</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.text}</span><br><small><span style='color: #00FF00;'>ID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.id}</span> <span style='color: #800080;'>|</span> <span style='color: #00FF00;'>Date</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.date}</span></small></p><hr>")
            try:
                full_info = await client(GetFullChannelRequest(main_entity))
                if full_info.full_chat.linked_chat_id:
                    linked_id = full_info.full_chat.linked_chat_id
                    linked_ent = await client.get_entity(linked_id)
                    all_data["linked"] = linked_ent
                    await smart_join(linked_id)
                    async for m in client.iter_messages(linked_ent, limit):
                        if m.text:
                            u_id_str = format_user_id(m.from_id) if m.from_id else "Unknown"
                            print(f"{get_time()}{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{m.text[:40]} {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{u_id_str}{colorama.Fore.WHITE}] [{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.MAGENTA}{m.date}{colorama.Fore.WHITE}]")
                            all_data["msgs"].append(f"<p><span style='color: #00FF00;'>[</span><span style='color: #FF8C00;'>CHAT</span><span style='color: #00FF00;'>]</span> <span style='color: #00FF00;'>Message</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.text}</span><br><small><span style='color: #00FF00;'>User</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u_id_str}</span> <span style='color: #800080;'>|</span> <span style='color: #00FF00;'>Date</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.date}</span></small></p><hr>")
            except: pass
        else:
            async for m in client.iter_messages(main_entity, limit):
                if m.text:
                    u_id_str = format_user_id(m.from_id) if m.from_id else "Unknown"
                    print(f"{get_time()}{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{m.text[:40]} {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{u_id_str}{colorama.Fore.WHITE}] [{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.MAGENTA}{m.date}{colorama.Fore.WHITE}]")
                    all_data["msgs"].append(f"<p><span style='color: #00FF00;'>[</span><span style='color: #FFD700;'>GROUP</span><span style='color: #00FF00;'>]</span> <span style='color: #00FF00;'>Message</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.text}</span><br><small><span style='color: #00FF00;'>User</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u_id_str}</span> <span style='color: #800080;'>|</span> <span style='color: #00FF00;'>Date</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.date}</span></small></p><hr>")
        return all_data
    except Exception: return all_data

async def generate_report(data, users, target_link):
    with open('report.html', 'w', encoding='utf-8') as f:
        f.write('<html lang="ru"><head><meta charset="utf-8"></head><body style="background-color: #0a0a0a; color: #00FF00; font-family: Consolas, monospace; padding: 20px;">')
        f.write(f"<h3><span style='color: #00FF00;'>Generated on</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{time.asctime()}</span></h3>")
        
        main_id = data['main'].id if data['main'] else "N/A"
        f.write(f"<h2><span style='color: #00FF00;'>Target</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{target_link} (ID: {main_id})</span></h2>")
        
        if data['linked']:
            f.write(f"<h2><span style='color: #00FF00;'>Linked Chat ID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{data['linked'].id}</span></h2>")

        f.write(f"<h2><span style='color: #00FF00;'>Total Messages</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{len(data['msgs'])}</span></h2>")
        f.write(f"<h2><span style='color: #00FF00;'>Total Users</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{len(users)}</span></h2><hr>")
        
        f.write("".join(data['msgs']))
        f.write("<h2><span style='color: #00FF00;'>Users</span><span style='color: #FF0000;'>:</span></h2>")
        f.write("".join(users))
        f.write("</body></html>")

async def func():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="ссылка на цель")
    argum = parser.parse_args()

    if argum.c:
        if os.path.exists('message.log'): os.remove('message.log')
        data = await get_messages(argum.c)
        if data["main"]:
            target_for_users = data["linked"] if data["linked"] else data["main"]
            users = []
            try:
                p = await client.get_participants(target_for_users)
                users = [f"<p><span style='color: #00FF00;'>User</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u.first_name}</span> <span style='color: #800080;'>|</span> <span style='color: #00FF00;'>ID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u.id}</span></p>" for u in p]
            except: pass
            
            await generate_report(data, users, argum.c)
            if os.path.exists('report.html'):
                caption = f"CH: {argum.c}\nTotal Users: {len(users)}\nTotal Messages: {len(data['msgs'])}\nDate: {time.asctime()}"
                await client.send_file(ADMIN_TAG, 'report.html', caption=caption)
                os.remove('report.html')
                now_prefix = f"{colorama.Fore.WHITE}[{colorama.Fore.BLUE}{time.asctime()}{colorama.Fore.WHITE}]"
                print(f"{now_prefix} {colorama.Fore.GREEN}Отчет отправлен {colorama.Fore.YELLOW}{ADMIN_TAG}")
                print(f"{now_prefix} {colorama.Fore.GREEN}Total messages {colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(data['msgs'])}")
                print(f"{now_prefix} {colorama.Fore.GREEN}Total users {colorama.Fore.RED} -> {colorama.Fore.YELLOW}{len(users)}")

async def main():
    global live_start_time
    await init_client()
    async with client:
        await func()
        live_start_time = datetime.now(timezone.utc)
        @client.on(events.NewMessage)
        async def live_monitor(event):
            if event.message.date < live_start_time: return
            if event.message.text:
                now_p = f"{colorama.Fore.WHITE}[{colorama.Fore.BLUE}{time.asctime()}{colorama.Fore.WHITE}]"
                print(f"{now_p}{colorama.Fore.WHITE}[{colorama.Fore.CYAN}LIVE{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{event.chat_id}{colorama.Fore.WHITE}]: {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{event.message.text[:50]}")
                with open('message.log', 'a', encoding='utf-8') as f:
                     f.write(f'[{time.asctime()}] ID: {event.chat_id}| Msg: {event.message.text[:50]}\n')
                with open('message.log', 'r', encoding='utf-8') as f:
                     logged = len(f.readlines())
                     print(f"{now_p} {colorama.Fore.GREEN}Logged messages{colorama.Fore.YELLOW}...{colorama.Fore.YELLOW}{logged}")

        final_p = f"{colorama.Fore.WHITE}[{colorama.Fore.BLUE}{time.asctime()}{colorama.Fore.WHITE}]"
        print(f"{final_p} {colorama.Fore.WHITE}[{colorama.Fore.CYAN}LIVE{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] Мониторинг запущен. Ctrl+C для выхода.")
        await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt: pass
