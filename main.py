import http.server
import socketserver
import json
import os
import sqlite3
from http import cookies

COOKIE_NAME = "book_rental_session"
BOOK_DB_PATH = "book_rental.sqlite"
USERS_DB_PATH = "users_db.sqlite"

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'login.html')
        elif self.path == '/register':
            self._send_response(200, 'register.html')
        elif self.path == '/books':
            self._send_response(200, 'book_rental.html')
        else:
            self._send_response(404, 'Page not found')

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                self._send_response(400, 'Invalid data')
                return
            if self.get_user_by_username(username):
                self._send_response(409, 'Username already exists')
                return
            self.register_user(username, password)
            self._send_response(200, 'Registration successful')

        elif self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            username = data.get('username')
            password = data.get('password')
            user = self.get_user_by_username(username)
            if user and user['password'] == password:
                session_id = os.urandom(16).hex()
                self.set_cookie(COOKIE_NAME, session_id)
                self._send_response(200, 'Login successful')
            else:
                self._send_response(401, 'Login failed')

        else:
            self._send_response(404, 'Endpoint not found')

    def set_cookie(self, key, value):
        if not hasattr(self, 'cookie'):
            self.cookie = cookies.SimpleCookie()
        self.cookie[key] = value
        self.cookie[key]['httponly'] = True

    def _send_response(self, status_code, page):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        if hasattr(self, 'cookie'):
            for cookie in self.cookie.values():
                self.send_header('Set-Cookie', cookie.OutputString())
        self.end_headers()
        with open(f'templates/{page}', 'rb') as file:
            self.wfile.write(file.read())

    def connect_db(self):
        return sqlite3.connect(DB_PATH)

    def create_users_table(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def get_user_by_username(self, username):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'password': user[2],
                'email':
user[3],
            }
        return None

    def register_user(self, username, password):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        conn.commit()
        conn.close()

def run():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
          