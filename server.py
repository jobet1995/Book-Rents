import http.server
import socketserver
import json
from users_db import create_users_table, register_user

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'login.html')
        elif self.path == '/register':
            self._send_response(200, 'register.html')
        elif self.path == '/forgot-password':
            self._send_response(200, 'forgot_password.html')
        else:
            self._send_response(404, 'Page not found')

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            username = data.get('username')
            password = data.get('password')
            register_user(username, password)
            self._send_response(200, 'Registration successful')

        elif self.path == '/forgot-password':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            email = data.get('email')
            self._send_response(200, f'Reset email sent to {email}')

        else:
            self._send_response(404, 'Endpoint not found')

    def _send_response(self, status_code, page):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(f'templates/{page}', 'rb') as file:
            self.wfile.write(file.read())

def run():
    create_users_table()

    PORT = 8080
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
      