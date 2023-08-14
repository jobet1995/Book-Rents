import sqlite3

db_path = "book_rental.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        publication_year INTEGER,
        ISBN TEXT,
        total_copies INTEGER,
        available_copies INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT,
        address TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS rentals (
        rental_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        book_id INTEGER,
        rental_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        returned_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS availability (
        availability_id INTEGER PRIMARY KEY,
        book_id INTEGER,
        available BOOLEAN,
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
''')


conn.commit()
conn.close()

print("Database created successfully.")
