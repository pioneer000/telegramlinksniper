from telethon import TelegramClient, events, functions, types
import re
import asyncio

api_id = ''
api_hash = ''
phone_number = ''

client = TelegramClient(None, api_id, api_hash)

join_link_pattern = re.compile(r'https://t\.me/\+([\w_]+)')

@client.on(events.NewMessage)
async def handler(event):
    if isinstance(event.chat, (types.Channel, types.Chat)) and event.text:
        match = join_link_pattern.search(event.text)
        if match:
            invite_hash = match.group(1)
            print(f"New join link detected: {invite_hash}")
            try:
                await client(functions.messages.ImportChatInviteRequest(hash=invite_hash))
                print(f"Successfully joined: {invite_hash}")
            except Exception as e:
                print(f"Failed to join link {invite_hash}: {e}")

async def main():
    await client.start(phone_number)
    print("Client is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
