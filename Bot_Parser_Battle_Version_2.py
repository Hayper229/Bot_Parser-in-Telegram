from telethon import TelegramClient, events, connection, errors
from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import Channel, User, PeerChannel, PeerUser
import os, colorama, argparse, asyncio, time

colorama.init(autoreset=True)

# --- CONFIG ---
api_id = API_ID
api_hash = 'API_HASH'
phone = '+PHONE_NUMBER'
ADMIN_TAG = '@AYour_UserName'
MY_ID = Your_ID

# Твой новый цвет (Ярко-голубой вместо обычного синего)
B = colorama.Fore.LIGHTBLUE_EX 

PROXY_LIST = [
    ('IP', PORT, 'SECRET'),
    ('IP', PORT, 'SECRET'),
    ('IP', PORT, 'SECRET')
]

client = None

async def init_client():
    global client
    for p_host, p_port, p_secret in PROXY_LIST:
        print(f"{B}[*] Пробую прокси: {p_host}:{p_port}")
        try:
            proxy = (p_host, p_port, p_secret)
            cl = TelegramClient(phone, api_id, api_hash, proxy=proxy, 
                                connection=connection.ConnectionTcpMTProxyIntermediate,
                                connection_retries=1, retry_delay=1)
            await cl.connect()
            if await cl.is_user_authorized():
                print(f"{colorama.Fore.GREEN}[+] OK: {p_host}")
                client = cl
                return
            await cl.disconnect()
        except: continue
    client = TelegramClient(phone, api_id, api_hash)
    await client.start(phone)

async def smart_join(target):
    try:
        if 't.me/joinchat/' in target or 't.me/+' in target:
            hash_code = target.split('/')[-1].replace('+', '')
            await client(ImportChatInviteRequest(hash_code))
        else:
            entity = await client.get_entity(target)
            await client(JoinChannelRequest(entity))
    except: pass

async def get_messages(channel_link):
    # Эта часть теперь работает быстро и безопасно для RAM
    users_map = {}
    msg_count = 0
    temp_file = 'temp_msgs.html'
    
    await smart_join(channel_link)
    main_entity = await client.get_entity(channel_link)
    print(f"{colorama.Fore.YELLOW}[+] Цель: {main_entity.title}. Сбор СМС...")

    is_broadcast = isinstance(main_entity, Channel) and getattr(main_entity, 'broadcast', False)
    linked_entity = None
    if is_broadcast:
        try:
            full = await client(GetFullChannelRequest(main_entity))
            if full.full_chat.linked_chat_id:
                linked_entity = await client.get_entity(full.full_chat.linked_chat_id)
                await smart_join(linked_entity)
        except: pass

    main_label = "CHANNEL" if is_broadcast else "GROUP"
    main_color = "#da70d6" if is_broadcast else "#FFD700"

    with open(temp_file, 'w', encoding='utf-8') as f:
        async def process(entity, label, tag_color):
            nonlocal msg_count
            try:
                async for m in client.iter_messages(entity):
                    if m.text:
                        msg_count += 1
                        # Твой оригинальный формат ID
                        u_id_str = str(m.from_id) if m.from_id else f"PeerChannel(channel_id={m.chat_id})"
                        
                        # ТЕРМИНАЛ: Твой оригинальный стиль
                        print(f"{colorama.Fore.WHITE}[{B}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] "
                              f"{colorama.Fore.GREEN}{m.text.strip()[:60]}... "
                              f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] "
                              f"[{colorama.Fore.MAGENTA}{u_id_str}{colorama.Fore.WHITE}] "
                              f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] "
                              f"[{colorama.Fore.MAGENTA}{m.date}{colorama.Fore.WHITE}]")

                        # HTML: Твой оригинальный стиль
                        f.write(f"<div style='margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 10px;'>"
                                f"<span style='color: #00FF00;'>[</span><span style='color: {tag_color};'>{label}</span><span style='color: #00FF00;'>]</span> "
                                f"<span style='color: #00FF00;'>Message</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.text}</span><br>"
                                f"<div style='margin-top: 10px; font-size: 0.9em;'>"
                                f"<span style='color: #00FF00;'>UserID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u_id_str}</span><br>"
                                f"<span style='color: #00FF00;'>Date of Dispatch</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.date}</span>"
                                f"</div></div>")

                        # Метод 2: Твоя проверка отправителя
                        if m.sender and isinstance(m.sender, User):
                            u = m.sender
                            if u.id != MY_ID and u.id not in users_map:
                                f_name = f"{u.first_name or ''} {u.last_name or ''}".strip()
                                users_map[u.id] = {
                                    "name": f_name if f_name else "Unknown",
                                    "user": u.username if u.username else "Unknown",
                                    "phone": u.phone if u.phone else "Unknown",
                                    "id_raw": str(m.from_id)
                                }
                    if msg_count % 100 == 0: await asyncio.sleep(0.05)
            except errors.FloodWaitError as e: await asyncio.sleep(e.seconds)

        await process(main_entity, main_label, main_color)
        if linked_entity: await process(linked_entity, "CHAT", "#FF8C00")

    return {"msg_count": msg_count, "users_map": users_map, "temp_file": temp_file, "linked": linked_entity, "main": main_entity}

async def func():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="target link")
    argum = parser.parse_args()

    if argum.c:
        data = await get_messages(argum.c)
        users_map = data["users_map"]
        
        # Метод 1: Твой оригинальный сбор участников
        target_for_parts = data["linked"] if data["linked"] else data["main"]
        print(f"{B}[*] МЕТОД 1: Сбор участников...")
        try:
            participants = await client.get_participants(target_for_parts)
            for u in participants:
                if u.id == MY_ID: continue
                if u.id not in users_map:
                    f_name = f"{u.first_name or ''} {u.last_name or ''}".strip()
                    users_map[u.id] = {
                        "name": f_name if f_name else "Unknown",
                        "user": u.username if u.username else "Unknown",
                        "phone": u.phone if u.phone else "Unknown",
                        "id_raw": str(u.id)
                    }
        except: pass

        # Формирование юзеров в HTML (Твой стиль)
        users_html = []
        for uid, info in users_map.items():
            u_disp = f"@{info['user']}" if info['user'] != "Unknown" else "Unknown"
            line = (
                f"<div style='border-bottom: 1px solid #444; margin-bottom: 20px; padding-bottom: 10px;'>"
                f"<span style='color: #00FF00;'>User</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{info['name']}</span><br>"
                f"<span style='color: #00FF00;'>Username</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u_disp}</span><br>"
                f"<span style='color: #00FF00;'>ID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{info['id_raw']}</span><br>"
                f"<span style='color: #00FF00;'>Phone number</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{info['phone']}</span>"
                f"</div>"
            )
            users_html.append(line)

        # Финальная сборка файла
        report_name = 'report.html'
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write('<html lang="ru"><head><meta charset="utf-8"></head><body style="background-color: #0a0a0a; color: #00FF00; font-family: Consolas, monospace; padding: 20px;">')
            f.write(f"<h3><span style='color: #00FF00;'>Generated on</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{time.asctime()}</span></h3>")
            f.write(f"<h2><span style='color: #00FF00;'>Total Messages</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{data['msg_count']}</span></h2>")
            f.write(f"<h2><span style='color: #00FF00;'>Total Users</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{len(users_html)}</span></h2><hr>")
            
            # Читаем сообщения из временного файла
            if os.path.exists(data['temp_file']):
                with open(data['temp_file'], 'r', encoding='utf-8') as tf:
                    f.write(tf.read())
                os.remove(data['temp_file'])

            f.write("<h2><span style='color: #00FF00;'>Users</span><span style='color: #FF0000;'>:</span></h2>")
            f.write("".join(users_html))
            f.write("</body></html>")

        # Отправка (Твой стиль)
        if os.path.exists(report_name):
            caption = f"CH: {argum.c}\nTotal messages: {data['msg_count']}\nTotal users: {len(users_html)}\nDate: {time.asctime()}"
            await client.send_file(ADMIN_TAG, report_name, caption=caption)
            os.remove(report_name)
            
            print(f"{colorama.Fore.WHITE}[{B}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Отчет отправлен {colorama.Fore.YELLOW}{ADMIN_TAG}")
            print(f"{colorama.Fore.WHITE}[{B}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total users  {colorama.Fore.RED}-> {colorama.Fore.YELLOW}{len(users_html)}")
            print(f"{colorama.Fore.WHITE}[{B}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total messages  {colorama.Fore.RED}-> {colorama.Fore.YELLOW}{data['msg_count']}")

async def main():
    await init_client()
    async with client:
        await func()
        print(f"{colorama.Fore.WHITE}[{B}{time.asctime()}{colorama.Fore.WHITE}] LIVE Active...")
        @client.on(events.NewMessage)
        async def live_monitor(event):
            if event.message.text:
                u_id = str(event.from_id) if event.from_id else f"PeerChannel(channel_id={event.chat_id})"
                print(f"{colorama.Fore.WHITE}[{B}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{B}LIVE{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{u_id}{colorama.Fore.WHITE}]: "
                      f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{event.message.text}")
        await client.run_until_disconnected()

if __name__ == '__main__':
    try: asyncio.run(main())
    except KeyboardInterrupt: pass

