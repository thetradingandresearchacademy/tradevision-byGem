import os
import json
from http.server import BaseHTTPRequestHandler
import requests

# This pulls directly from the Vercel Settings you just saved
SUPABASE_URL = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = json.loads(self.rfile.read(content_length))
            symbol = post_data.get('symbol', 'RELIANCE').upper()

            # The Brain: Calling your Symbol Edge Function
            target_url = f"{SUPABASE_URL}/functions/v1/swinglab-engine"
            
            headers = {
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(target_url, headers=headers, json={"symbol": symbol})
            response_data = response.json()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
