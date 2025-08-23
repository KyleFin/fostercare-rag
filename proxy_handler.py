#!/usr/bin/env python3
import http.server
import socketserver
import os
import threading
import subprocess
import sys
import re
import urllib.request
import urllib.error
import json
from urllib.parse import urlparse

# Custom request handler for React SPA routing
class ReactAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if this is an API request that should be proxied
        if self.path.startswith("/api/"):
            self.proxy_request("GET")
            return
            
        # If the path doesn't point to a file or directory that exists,
        # serve index.html instead (for React routing)
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            # Check if it's a direct directory request without index.html
            if os.path.isdir(path):
                index_path = os.path.join(path, "index.html")
                if os.path.exists(index_path):
                    return super().do_GET()
            # Otherwise serve the React app's index.html for client-side routing
            self.path = "/index.html"
        return super().do_GET()
    
    def do_POST(self):
        # Proxy all POST requests to the API server
        if self.path.startswith("/api/"):
            self.proxy_request("POST")
            return
        
        # Handle other POST requests (if any)
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found")
    
    def proxy_request(self, method):
        # Get content length for POST requests
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None
        
        # Create API URL
        api_url = f"http://localhost:8000{self.path}"
        
        try:
            # Create request
            req = urllib.request.Request(api_url, method=method)
            
            # Copy headers
            for header, value in self.headers.items():
                if header.lower() not in ["host", "content-length"]:
                    req.add_header(header, value)
            
            # Add body for POST requests
            if method == "POST" and body:
                req.add_header("Content-Length", str(len(body)))
                req.data = body
            
            # Send request to API server
            response = urllib.request.urlopen(req)
            
            # Send response back to client
            self.send_response(response.status)
            
            # Copy response headers
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            
            # Stream response body
            self.wfile.write(response.read())
            
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for header, value in e.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(str(e).encode())

def serve_frontend():
    os.chdir("/app/frontend/build")
    with socketserver.TCPServer(("", 3000), ReactAppHandler) as httpd:
        print("React frontend server running on port 3000")
        httpd.serve_forever()

def serve_api():
    os.chdir("/app")
    subprocess.run([sys.executable, "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    # Start frontend server in a separate thread
    frontend_thread = threading.Thread(target=serve_frontend, daemon=True)
    frontend_thread.start()
    
    # Start API server in main thread
    serve_api()
