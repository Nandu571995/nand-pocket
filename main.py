import os
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_listener  # NOTE: renamed to listener (runs in main thread)

def dummy_http_server():
    port = int(os.environ.get("PORT", 10000))
    with TCPServer(("0.0.0.0", port), SimpleHTTPRequestHandler) as httpd:
        print(f"🟢 Dummy server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("📦 Starting Pocket Option Signal Bot")

    # Start dummy server and pocket bot in background
    threading.Thread(target=dummy_http_server, daemon=True).start()
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # Run Telegram bot listener in main thread (IMPORTANT)
    run_telegram_listener()
