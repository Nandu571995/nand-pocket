import os
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from pocket_bot import start_pocket_bot
from telegram_bot import run_telegram_bot

def dummy_http_server():
    port = int(os.environ.get("PORT", 10000))
    with TCPServer(("0.0.0.0", port), SimpleHTTPRequestHandler) as httpd:
        print(f"🟢 Dummy server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("📦 Starting Pocket Option Signal Bot with Telegram")

    # Start dummy HTTP server (required for Render)
    threading.Thread(target=dummy_http_server, daemon=True).start()

    # Start Pocket Option signal bot in a separate thread
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # Run Telegram bot in MAIN thread to avoid conflict
    run_telegram_bot()

    # Sleep loop not needed — Telegram bot is blocking and keeps alive
