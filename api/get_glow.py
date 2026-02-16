from http.server import BaseHTTPRequestHandler
import json
from supabase import create_client

# Vercel picks these up from your Environment Variables
url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
supabase = create_client(url, key)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Check for the User's JWT (Auth Token)
        auth_header = self.headers.get('Authorization')
        if not auth_header:
            self.send_response(401)
            return

        # 2. Fetch the latest Engine Signal for the User
        # This pulls the Fused Score + Forward Trajectory we just built
        data = json.loads(self.rfile.read(self.path_content_length))
        symbol = data.get('symbol', 'NIFTY_50')

        result = supabase.table("engine_signals") \
            .select("*") \
            .eq("symbol", symbol) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result.data[0]).encode())
