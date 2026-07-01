from telethon.sync import TelegramClient
import csv, time

api_id   = 33163177
api_hash = '100290ab0dfdb108d4100550810d11b8'
chat     = 'https://t.me/+2DKa_aPM9gY0ZTQy'

client = TelegramClient('tg_session', api_id, api_hash)
client.start()

print("Собираю сообщения...")
seen = {}

for msg in client.iter_messages(chat, reverse=True):
    if not msg.sender_id:
        continue
    if msg.sender_id not in seen:
        try:
            s = msg.get_sender()
            seen[msg.sender_id] = {
                'id':       msg.sender_id,
                'username': getattr(s, 'username', '') or '',
                'name':     f"{getattr(s,'first_name','') or ''} {getattr(s,'last_name','') or ''}".strip()
            }
            if len(seen) % 100 == 0:
                print(f"Найдено уникальных: {len(seen)}")
        except:
            seen[msg.sender_id] = {'id': msg.sender_id, 'username': '', 'name': ''}
        time.sleep(0.3)

with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['id', 'username', 'name'])
    w.writeheader()
    w.writerows(seen.values())

print(f"\nГотово! Уникальных пользователей: {len(seen)}")
print("Файл сохранён: result.csv")
