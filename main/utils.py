import httpx
import threading
import asyncio
import html  # Для безопасной отправки текста
from django.conf import settings


def send_telegram_notification(message):
    token = settings.TELEGRAM_BOT_TOKEN
    admin_ids = settings.TELEGRAM_ADMIN_IDS
    if not token:
        print("TELEGRAM_BOT_TOKEN не задан, уведомление пропущено")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    safe_message = html.escape(message)

    async def send_async():
        async with httpx.AsyncClient() as client:
            for chat_id in admin_ids:
                payload = {
                    "chat_id": chat_id,
                    "text": message, # Если хочешь жирный шрифт и т.д., оставь message, но следи за тегами
                    "parse_mode": "HTML"
                }
                try:
                    response = await client.post(url, json=payload, timeout=5.0)
                    print(f"Отправка на {chat_id}: {response.status_code}")
                except Exception as e:
                    print(f"Ошибка при отправке пользователю {chat_id}: {e}")

    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_async())
        loop.close()

    threading.Thread(target=run_in_thread, daemon=True).start()