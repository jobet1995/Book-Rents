import http.server
import socketserver
import sqlite3
import json

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

def run():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()         