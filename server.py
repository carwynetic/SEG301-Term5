import http.server
import socketserver
import webbrowser
import os
import sys

# Configure UTF-8 for console output
sys.stdout.reconfigure(encoding='utf-8')

PORT = 8001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and caching headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def run():
    global PORT
    os.chdir(DIRECTORY)
    
    server = None
    for attempt_port in range(PORT, PORT + 20):
        try:
            server = http.server.ThreadingHTTPServer(("", attempt_port), Handler)
            PORT = attempt_port
            break
        except OSError:
            continue

    if not server:
        print("❌ Không tìm thấy cổng khả dụng từ 8001-8020.")
        return

    url = f"http://localhost:{PORT}"
    print("=" * 65)
    print("🚀 SEG301 - HỆ THỐNG ÔN THI SEARCH ENGINES TOÀN DIỆN (17 CHAPTERS)")
    print(f"📡 Máy chủ đang chạy tại: {url}")
    print(f"📁 Thư mục gốc: {DIRECTORY}")
    print("=" * 65)
    print("🌐 Đang tự động mở trình duyệt web...")
    print("Nhấn Ctrl + C để dừng máy chủ.")

    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"⚠️ Không thể tự mở trình duyệt ({e}), vui lòng mở thủ công: {url}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng máy chủ cục bộ. Tạm biệt!")
        server.server_close()

if __name__ == "__main__":
    run()
