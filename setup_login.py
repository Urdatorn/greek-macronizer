import sqlite3
from werkzeug.security import generate_password_hash

def create_db():
    conn = sqlite3.connect('users.db')  # This will create the database file and open a connection
    cursor = conn.cursor()

    # Create the table for storing users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')

    # Add the first user
    username = 'urdatorn'
    password = generate_password_hash('dfgj2398efgoiws?')  # Hash the password for secure storage

    # Insert the user into the table
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database and user have been set up successfully.")
