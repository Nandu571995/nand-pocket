import os
import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

from pocket_bot import start_pocket_bot
from telegram_bot import run_bot  # Function renamed in telegram_bot.py

def dummy_http_server():
    port = int(os.environ.get("PORT", 10000))
    with TCPServer(("0.0.0.0", port), SimpleHTTPRequestHandler) as httpd:
        print(f"🟢 Dummy server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("📦 Starting Pocket Option Signal Bot with Telegram")

    # Start dummy HTTP server (Render requirement)
    threading.Thread(target=dummy_http_server, daemon=True).start()

    # Start Pocket Option bot thread
    threading.Thread(target=start_pocket_bot, daemon=True).start()

    # Run Telegram bot (blocking thread)
    run_bot()
