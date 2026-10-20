import http.server
import socketserver
import os
import sys
import json
import urllib.parse

# Windows cp1251 konsollarida UTF-8 ni ta'minlash
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DIRECTORY, "js", "data.js")
REQUESTS_FILE = os.path.join(DIRECTORY, "user_requests.json")

def load_gadgets_from_js():
    """js/data.js dan gadjetlar ro'yxatini yuklaydi"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            # export const GADGETS_DATA = [...]; qismini ajratib olish
            start_marker = "export const GADGETS_DATA = ["
            start_idx = content.find(start_marker)
            if start_idx != -1:
                start_json = start_idx + len("export const GADGETS_DATA = ")
                # massiv tugash joyi
                end_marker = "export const CATEGORIES"
                end_idx = content.find(end_marker, start_json)
                if end_idx != -1:
                    raw_data = content[start_json:end_idx].strip()
                    if raw_data.endswith(";"):
                        raw_data = raw_data[:-1].strip()
                    # Python JSON ga moslashtirish (agar kerak bo'lsa)
                    # Oddiyroq va barqarorroq: js/data.json faylida ham sinxron saqlaymiz
    except Exception as e:
        print(f"Xatolik data.js o'qishda: {e}")
    return []

class RealTechRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Brauzer keshlashini o'chirish (o'zgarishlar darhol ko'rinishi uchun)
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        # JavaScript fayllar uchun to'g'ri MIME type
        if self.path.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
        super().end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # ==================== BACKEND API ====================
        
        # 1. /api/search?q=...
        if path == "/api/search":
            query = query_params.get("q", [""])[0].strip().lower()
            devices = self.get_all_devices()
            
            if not query:
                results = devices
            else:
                results = []
                for d in devices:
                    name_match = query in d.get("name", "").lower()
                    short_match = query in d.get("shortName", "").lower()
                    brand_match = query in d.get("brand", "").lower()
                    cat_match = query in d.get("category", "").lower()
                    alias_match = any(query in a.lower() or a.lower() in query for a in d.get("aliases", []))
                    feature_match = any(query in f.get("feature", "").lower() for f in d.get("howItWorks", []))

                    if name_match or short_match or brand_match or cat_match or alias_match or feature_match:
                        results.append(d)

            # Agar topilmasa, YouTube qidiruv havolasi va tavsiyalarni qaytaramiz
            response_data = {
                "success": True,
                "query": query,
                "count": len(results),
                "devices": results,
                "youtubeSearchUrl": f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}+real+battery+drain+test",
                "youtubeReviewUrl": f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}+uzbekcha+sharh"
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
            return

        # 2. /api/devices
        if path == "/api/devices":
            devices = self.get_all_devices()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "count": len(devices), "devices": devices}, ensure_ascii=False).encode("utf-8"))
            return

        # 3. /api/stats
        if path == "/api/stats":
            devices = self.get_all_devices()
            stats = {
                "totalGadgets": len(devices),
                "smartphones": len([d for d in devices if d.get("category") == "Smartfonlar"]),
                "watches": len([d for d in devices if d.get("category") == "Aqlli soatlar"]),
                "earbuds": len([d for d in devices if d.get("category") == "Quloqchinlar"]),
                "verifiedSourcesCount": sum(len(d.get("sources", [])) for d in devices)
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(stats, ensure_ascii=False).encode("utf-8"))
            return

        # Boshqa so'rovlar uchun statik fayllarni uzatish
        super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # 4. /api/request-model — Foydalanuvchi yangi gadjet qo'shish so'rovi yuborishi
        if path == "/api/request-model":
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_body)
                model_name = data.get("modelName", "").strip()
                contact = data.get("contact", "").strip()
                
                # Faylga saqlab qo'yish
                requests = []
                if os.path.exists(REQUESTS_FILE):
                    try:
                        with open(REQUESTS_FILE, "r", encoding="utf-8") as f:
                            requests = json.load(f)
                    except Exception:
                        requests = []
                
                new_entry = {
                    "modelName": model_name,
                    "contact": contact,
                    "date": "2026-10-20"
                }
                requests.append(new_entry)

                with open(REQUESTS_FILE, "w", encoding="utf-8") as f:
                    json.dump(requests, f, ensure_ascii=False, indent=2)

                # Telegram Botga yuborish (agar sozlagan bo'lsa)
                tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
                tg_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
                
                if tg_token and tg_chat_id:
                    try:
                        msg_text = f"🔔 RealTech Uz — Yangi Gadjet So'rovi!\n\n📱 Model: {model_name}\n👤 Aloqa: {contact or 'Kiritilmagan'}\n📅 Sana: 2026-10-20"
                        tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
                        req_data = urllib.parse.urlencode({"chat_id": tg_chat_id, "text": msg_text}).encode("utf-8")
                        urllib.request.urlopen(tg_url, data=req_data, timeout=5)
                    except Exception as tg_err:
                        print(f"Telegram yuborishda xatolik: {tg_err}")

                res = {"success": True, "message": f"'{model_name}' bo'yicha so'rovingiz qabul qilindi! Tez orada platformaga kiritiladi."}
            except Exception as e:
                res = {"success": False, "error": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        super().do_POST()

    def get_all_devices(self):
        """Ma'lumotlar bazasi JSON faylidan o'qish"""
        db_path = os.path.join(DIRECTORY, "data", "gadgets.json")
        if os.path.exists(db_path):
            try:
                with open(db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

def run_server():
    os.chdir(DIRECTORY)
    port = PORT
    for attempt in range(5):
        try:
            with socketserver.TCPServer(("", port), RealTechRequestHandler) as httpd:
                print("==================================================")
                print(f"[RealTech Uz] Backend & Frontend server ishlamoqda!")
                print(f"Manzil: http://localhost:{port}")
                print(f"API Manzillari:")
                print(f"  - http://localhost:{port}/api/devices")
                print(f"  - http://localhost:{port}/api/search?q=iwatch")
                print(f"  - http://localhost:{port}/api/stats")
                print("==================================================")
                print("Chiqish uchun Ctrl+C bosing...")
                sys.stdout.flush()
                httpd.serve_forever()
                break
        except OSError:
            port += 1

if __name__ == "__main__":
    run_server()
