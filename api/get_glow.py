import os
import json
from http.server import BaseHTTPRequestHandler
import requests

# Still pull from Vercel Env Vars (Securely)
SUPABASE_URL = os.environ.get("https://tfpscbilfwekzvvktinm.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmcHNjYmlsZndla3p2dmt0aW5tIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDg5NDI0NCwiZXhwIjoyMDg2NDcwMjQ0fQ.PrlLd396pU_lBMbIws-Dl17u2Eu-UUgrjZGgFbqTIjI")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = json.loads(self.rfile.read(content_length))
            
            headers = {"Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
            url = f"{SUPABASE_URL}/functions/v1/swinglab-engine"
            
            response = requests.post(url, headers=headers, json={"symbol": post_data.get('symbol')})
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response.json()).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
