import asyncio
import csv
import os
from telethon import TelegramClient
from telethon.tl.types import User

API_ID = int(os.environ.get("TG_API_ID", 0))
API_HASH = os.environ.get("TG_API_HASH", "")
GROUP_LINK = os.environ.get("TG_GROUP", "")
OUTPUT_FILE = "members.csv"


async def parse_members(client: TelegramClient, group_link: str):
    entity = await client.get_entity(group_link)
    print(f"Группа: {getattr(entity, 'title', group_link)}")

    seen = {}
    total = 0

    async for message in client.iter_messages(entity, limit=None):
        sender = message.sender
        if not isinstance(sender, User) or sender.id in seen or sender.bot:
            continue
        seen[sender.id] = {
            "id": sender.id,
            "username": sender.username or "",
            "first_name": sender.first_name or "",
            "last_name": sender.last_name or "",
            "phone": sender.phone or "",
        }
        total += 1
        if total % 100 == 0:
            print(f"  Найдено уникальных авторов: {len(seen)} (обработано сообщений: {total})")

    return list(seen.values())


def save_csv(users: list, path: str):
    if not users:
        print("Никого не нашли.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "username", "first_name", "last_name", "phone"])
        writer.writeheader()
        writer.writerows(users)
    print(f"Сохранено {len(users)} пользователей → {path}")


async def main():
    if not API_ID or not API_HASH:
        print("Установи переменные: TG_API_ID, TG_API_HASH, TG_GROUP")
        return

    group = GROUP_LINK or input("Ссылка на группу: ").strip()

    async with TelegramClient("session", API_ID, API_HASH) as client:
        users = await parse_members(client, group)
        save_csv(users, OUTPUT_FILE)


if __name__ == "__main__":
    asyncio.run(main())
