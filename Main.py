import http.server
import socketserver
import os
import subprocess

# === Настройки ===
PORT = 8080
FOLDER = "Main"

# === Запуск сервера ===
os.chdir(FOLDER)
handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Сайт запущен на http://localhost:{PORT}")

    # === Автоматический запуск ngrok ===
    try:
        subprocess.Popen(["ngrok", "http", str(PORT)])
        print("Открой ngrok URL из консоли ниже ↓")
    except FileNotFoundError:
        print("⚠ Не найден ngrok. Установи его с https://ngrok.com/ и добавь в PATH.")

    httpd.serve_forever()
