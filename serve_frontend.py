import http.server
import socketserver
import os

PORT = 5500
os.chdir('frontend')

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.js': 'application/javascript',
})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Frontend server running at http://localhost:{PORT}")
    print("Open http://localhost:5500 in your browser")
    httpd.serve_forever()
