from telethon import TelegramClient, events, connection, errors
from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import Channel, User, PeerChannel
import os, colorama, argparse, asyncio, time

colorama.init(autoreset=True)

api_id = API_ID
api_hash = 'API_HASH'
phone = '+PHONE NUMBER'
ADMIN_TAG = '@YOUR_USERNAME'
MY_ID = YOUR_ID

PROXY_LIST = [
    ('IP', PORT, 'SECRET'),
    ('IP', PORT, 'SECRET'),
    ('IP', PORT, 'SECRET')
]

client = None

async def init_client():
    global client
    for p_host, p_port, p_secret in PROXY_LIST:
        print(f"{colorama.Fore.LIGHTMAGENTA_EX}[*] Пробую прокси: {p_host}:{p_port}")
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
    users_map = {} 
    all_msgs_objects = [] 
    msg_count = 0
    temp_msgs_file = 'temp_msgs.html'
    report_file = 'report.html'
    
    try:
        await smart_join(channel_link)
        main_entity = await client.get_entity(channel_link)
        print(f"{colorama.Fore.YELLOW}[+] Цель: {main_entity.title}. Начинаю сбор...")

        is_broadcast = isinstance(main_entity, Channel) and getattr(main_entity, 'broadcast', False)
        linked_entity = None
        if is_broadcast:
            try:
                full = await client(GetFullChannelRequest(main_entity))
                if full.full_chat.linked_chat_id:
                    linked_entity = await client.get_entity(full.full_chat.linked_chat_id)
                    await smart_join(linked_entity)
            except: pass

        # --- ШАГ 1: СБОР СМС ---
        print(f"{colorama.Fore.LIGHTMAGENTA_EX}[*] ШАГ 1: Сбор всех сообщений...")
        main_label = "CHANNEL" if is_broadcast else "GROUP"
        main_color = "#da70d6" if is_broadcast else "#FFD700"

        with open(temp_msgs_file, 'w', encoding='utf-8') as f:
            async def process_msgs(entity, label, tag_color):
                nonlocal msg_count
                try:
                    async for m in client.iter_messages(entity):
                        if m.text:
                            msg_count += 1
                            all_msgs_objects.append(m)
                            u_id_str = f"PeerChannel(channel_id={m.sender_id or m.chat_id})"
                            
                            # ТЕРМИНАЛ (Light Magenta стиль)
                            print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] "
                                  f"{colorama.Fore.GREEN}{m.text.strip()[:60]}... "
                                  f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] "
                                  f"[{colorama.Fore.MAGENTA}{u_id_str}{colorama.Fore.WHITE}] "
                                  f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Date of Dispatch{colorama.Fore.WHITE}] "
                                  f"[{colorama.Fore.MAGENTA}{m.date}{colorama.Fore.WHITE}]")

                            f.write(f"<div style='margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 10px;'>"
                                    f"<span style='color: #00FF00;'>[</span><span style='color: {tag_color};'>{label}</span><span style='color: #00FF00;'>]</span> "
                                    f"<span style='color: #00FF00;'>Message</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.text}</span><br>"
                                    f"<div style='margin-top: 10px; font-size: 0.9em;'>"
                                    f"<span style='color: #00FF00;'>UserID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u_id_str}</span><br>"
                                    f"<span style='color: #00FF00;'>Date of Dispatch</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{m.date}</span>"
                                    f"</div></div>")
                        if msg_count % 100 == 0: await asyncio.sleep(0.05)
                except errors.FloodWaitError as e: await asyncio.sleep(e.seconds)

            await process_msgs(main_entity, main_label, main_color)
            if linked_entity:
                await process_msgs(linked_entity, "CHAT", "#FF8C00")

        # --- ШАГ 2: МЕТОД 1 ---
        async def collect_meth1(entity):
            print(f"{colorama.Fore.LIGHTMAGENTA_EX}[*] МЕТОД 1: Сбор участников для: {getattr(entity, 'title', 'Unknown')}...")
            try:
                async for u in client.iter_participants(entity):
                    if u.id == MY_ID: continue
                    if u.id not in users_map:
                        f_name = f"{u.first_name or ''} {u.last_name or ''}".strip()
                        users_map[u.id] = {"name": f_name or "Unknown", "user": u.username or "Unknown", "phone": u.phone or "Unknown"}
            except: pass

        await collect_meth1(main_entity)
        if linked_entity: await collect_meth1(linked_entity)

        # --- ШАГ 3: МЕТОД 2 ---
        print(f"{colorama.Fore.LIGHTMAGENTA_EX}[*] МЕТОД 2: Анализ авторов из собранных СМС...")
        for m in all_msgs_objects:
            if m.sender and isinstance(m.sender, User) and m.sender.id != MY_ID:
                if m.sender.id not in users_map:
                    f_name = f"{m.sender.first_name or ''} {m.sender.last_name or ''}".strip()
                    users_map[m.sender.id] = {"name": f_name or "Unknown", "user": m.sender.username or "Unknown", "phone": m.sender.phone or "Unknown"}

        # ФИНАЛЬНЫЙ РЕПОРТ
        with open(report_file, 'w', encoding='utf-8') as rf:
            rf.write('<html lang="ru"><head><meta charset="utf-8"></head><body style="background-color: #0a0a0a; color: #00FF00; font-family: Consolas, monospace; padding: 20px;">')
            rf.write(f"<h3><span style='color: #00FF00;'>Generated on</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{time.asctime()}</span></h3>")
            rf.write(f"<h2><span style='color: #00FF00;'>Total Messages</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{msg_count}</span></h2>")
            rf.write(f"<h2><span style='color: #00FF00;'>Total Users</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{len(users_map)}</span></h2><hr>")
            
            if os.path.exists(temp_msgs_file):
                with open(temp_msgs_file, 'r', encoding='utf-8') as tf: rf.write(tf.read())
                os.remove(temp_msgs_file)

            rf.write("<h2><span style='color: #00FF00;'>Users</span><span style='color: #FF0000;'>:</span></h2>")
            for uid, info in users_map.items():
                u_disp = f"@{info['user']}" if info['user'] != "Unknown" else "Unknown"
                rf.write(f"<div style='border-bottom: 1px solid #444; margin-bottom: 20px; padding-bottom: 10px;'>"
                         f"<span style='color: #00FF00;'>User</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{info['name']}</span><br>"
                         f"<span style='color: #00FF00;'>Username</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{u_disp}</span><br>"
                         f"<span style='color: #00FF00;'>ID</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>PeerChannel(channel_id={uid})</span><br>"
                         f"<span style='color: #00FF00;'>Phone number</span><span style='color: #FF0000;'>:</span> <span style='color: #FFFF00;'>{info['phone']}</span></div>")
            rf.write("</body></html>")

        if os.path.exists(report_file):
            caption = (
                f"CH: {channel_link}\n"
                f"Total messages: {msg_count}\n"
                f"Total users: {len(users_map)}\n"
                f"Date: {time.asctime()}"
            )
            await client.send_file(ADMIN_TAG, report_file, caption=caption)
            os.remove(report_file)
            
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Отчет отправлен {colorama.Fore.YELLOW}{ADMIN_TAG}")
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total users  {colorama.Fore.RED}-> {colorama.Fore.YELLOW}{len(users_map)}")
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}{time.asctime()}{colorama.Fore.WHITE}] {colorama.Fore.GREEN}Total messages  {colorama.Fore.RED}-> {colorama.Fore.YELLOW}{msg_count}")

    except Exception as e: print(f"Ошибка: {e}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="target link")
    args = parser.parse_args()
    await init_client()
    if args.c: await get_messages(args.c)
    print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}{time.asctime()}{colorama.Fore.WHITE}] LIVE Active...")
    @client.on(events.NewMessage)
    async def live_monitor(event):
        if event.message.text:
            u_id = f"PeerChannel(channel_id={event.sender_id or event.chat_id})"
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}{time.asctime()}{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.LIGHTMAGENTA_EX}LIVE{colorama.Fore.WHITE}]{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}UserID{colorama.Fore.WHITE}] [{colorama.Fore.MAGENTA}{u_id}{colorama.Fore.WHITE}]: "
                  f"{colorama.Fore.WHITE}[{colorama.Fore.YELLOW}Message{colorama.Fore.WHITE}] {colorama.Fore.GREEN}{event.message.text}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try: asyncio.run(main())
    except KeyboardInterrupt: pass
