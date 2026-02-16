import os
import json
from http.server import BaseHTTPRequestHandler
import requests

# These are pulled SECURELY from Vercel Environment Variables
SUPABASE_URL = os.environ.get("https://tfpscbilfwekzvvktinm.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRmcHNjYmlsZndla3p2dmt0aW5tIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDg5NDI0NCwiZXhwIjoyMDg2NDcwMjQ0fQ.PrlLd396pU_lBMbIws-Dl17u2Eu-UUgrjZGgFbqTIjI")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = json.loads(self.rfile.read(content_length))
            symbol = post_data.get('symbol', 'RELIANCE').upper()

            # THE FIX: Pointing to your Symbol Edge Function
            target_url = f"{SUPABASE_URL}/functions/v1/swinglab-engine"
            headers = {"Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json"}
            
            # Handshake with the Astro-Technical Engine
            response = requests.post(target_url, headers=headers, json={"symbol": symbol})
            response_data = response.json()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            # SAFETY: Always return JSON so the frontend doesn't crash on "Unexpected token A"
            self.send_response(200) # Send 200 with error data to prevent browser-level 500 breaks
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e), "historical": [], "forecast": []}).encode())
