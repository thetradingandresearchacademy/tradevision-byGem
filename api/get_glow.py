import os
import json
from http.server import BaseHTTPRequestHandler
import requests

# SECURE: These must be set in Vercel Project Settings (Environment Variables)
SUPABASE_URL = os.environ.get("https://tfpscbilfwekzvvktinm.supabase.coL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmcHNjYmlsZndla3p2dmt0aW5tIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDg5NDI0NCwiZXhwIjoyMDg2NDcwMjQ0fQ.PrlLd396pU_lBMbIws-Dl17u2Eu-UUgrjZGgFbqTIjI")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = json.loads(self.rfile.read(content_length))
        symbol = post_data.get('symbol', 'NIFTY_50')

        # Calling your Supabase Edge Function "Brain" (The 55/45 logic)
        edge_url = f"{SUPABASE_URL}https://tfpscbilfwekzvvktinm.supabase.co/functions/v1/Simulate-3"
        headers = {
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(edge_url, headers=headers, json={"symbol": symbol})
            response.raise_for_status()
            data = response.json()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
