import http.server
import socketserver
import sqlite3
import json
import threading
import time
import unittest
import requests

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            books = self.get_books()

            self.wfile.write(json.dumps(books).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not Found".encode())

    def do_POST(self):
        if self.path == '/books':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            self.add_book(data)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Book added successfully'}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not Found".encode())

    def do_DELETE(self):
        if self.path.startswith('/books/'):
            _, _, book_id = self.path.partition('/books/')
            self.delete_book(int(book_id))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Book deleted successfully'}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Not Found".encode())

    def get_books(self):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

        conn.close()
        book_list = []
        for book in books:
            book_data = {
                'book_id': book[0],
                'title': book[1],
                'author': book[2],
                'genre': book[3],
                'publication_year': book[4],
                'ISBN': book[5],
                'total_copies': book[6],
                'available_copies': book[7]
            }
            book_list.append(book_data)

        return book_list

    def add_book(self, data):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO books (title, author, genre, publication_year, ISBN, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['title'], data['author'], data['genre'], data['publication_year'], data['ISBN'], data['total_copies'], data['available_copies']))

        conn.commit()
        conn.close()

    def delete_book(self, book_id):
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))

        conn.commit()
        conn.close()

    def connect_db(self):
        return sqlite3.connect("book_rental.db")

def run_test_server():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Test server running at port {PORT}")
        httpd.serve_forever()

class TestBookRentalAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=run_test_server)
        cls.server_thread.start()
        time.sleep(1)  # Wait for the server to start

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.join()

    def test_get_books(self):
        response = requests.get('http://localhost:8080/books')
        self.assertEqual(response.status_code, 200)
        books = response.json()
        self.assertIsInstance(books, list)

    def test_add_book(self):
        new_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'publication_year': 2023,
            'ISBN': '1234567890',
            'total_copies': 5,
            'available_copies': 5
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8080/books', data=json.dumps(new_book), headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_delete_book(self):
        new_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'publication_year': 2023,
            'ISBN': '1234567890',
            'total_copies': 5,
            'available_copies': 5
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://localhost:8080/books', data=json.dumps(new_book), headers=headers)
        self.assertEqual(response.status_code, 201)
        book_id = response.json().get('book_id')

        response = requests.delete(f'http://localhost:8080/books/{book_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
      