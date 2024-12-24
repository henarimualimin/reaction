import asyncio
import random
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
from telethon.errors import RPCError
from flask import Flask
import sqlite3

# API ID dan API Hash dari aplikasi Telegram Anda
api_id = '14674456'
api_hash = '685dd82ac49613a292458096026cfb64'

# Daftar bot token untuk beberapa bot
bot_tokens = [
    '7292633624:AAHtTZPvgIgfQf_BHYa4mUqFODCnyeHHVIs',
    '7371462594:AAFE-4zieMuo5ZEsiADMV4a4PjV62aQCzko',
    '7397422472:AAG5ysCQqWsK7EhTHT_pkm2dZWx41EOYHk8'
]

# Daftar channel yang akan dimonitor
channels = ['@airdropdiggerid']

# Reaksi yang akan dikirim
reactions = ['⚡️', '🐳', '🔥']

# Fungsi untuk memulai bot reaksi
async def start_bot(bot_token):
    client = TelegramClient('bot_' + bot_token.split(':')[0], api_id, api_hash)
    try:
        await client.start(bot_token=bot_token)
    except sqlite3.OperationalError as e:
        print(f'Bot {bot_token}: Database is locked, skipping to next bot...')
        return

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        message_id = event.message.id
        chat_id = event.message.peer_id.channel_id

        # Menambahkan jeda 20 detik sebelum mereaksi
        await asyncio.sleep(20)

        # Memilih reaksi acak dari daftar
        reaction = random.choice(reactions)

        try:
            await client(SendReactionRequest(
                peer=event.message.to_id,
                msg_id=message_id,
                reaction=[ReactionEmoji(emoticon=reaction)]
            ))
            print(f'Bot {bot_token}: Reaksi {reaction} ditambahkan ke post {message_id} di {chat_id}')
            await asyncio.sleep(30)  # Jeda 10 detik antara pengiriman reaksi
        except RPCError as e:
            print(f'Bot {bot_token}: Error saat menambahkan reaksi {reaction}: {e}')
        except Exception as e:
            print(f'Bot {bot_token}: Error saat menambahkan reaksi: {e}')

    print(f'Bot {bot_token} berjalan...')
    await client.run_until_disconnected()

# Fungsi utama untuk menjalankan semua bot
async def main():
    tasks = [start_bot(bot_token) for bot_token in bot_tokens]
    await asyncio.gather(*tasks)

# Tambahkan server Flask agar kompatibel dengan Vercel
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Reaction is running!"

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: asyncio.run(main())).start()
    app.run(host="0.0.0.0", port=8000)
