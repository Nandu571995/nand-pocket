import os
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot_background

def dummy_http_server():
    port = int(os.environ.get("PORT", 10000))
    with TCPServer(("0.0.0.0", port), SimpleHTTPRequestHandler) as httpd:
        print(f"🟢 Dummy server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("📦 Starting Pocket Option Signal Bot (Telegram only)")

    threading.Thread(target=dummy_http_server, daemon=True).start()
    threading.Thread(target=start_pocket_bot, daemon=True).start()
    threading.Thread(target=run_telegram_bot_background, daemon=True).start()

    while True:
        time.sleep(10)
