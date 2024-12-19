import sqlite3
from sqlite3 import Error
import os

def create_connection():
    """Create a database connection to a SQLite database"""
    try:
        # Attempt to connect to the SQLite database file 'inpainting.db'.
        conn = sqlite3.connect('inpainting.db')
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db():
    """Initialize the database with required tables"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor() # Create a cursor object to execute SQL commands.
            
            # Create table for storing image pairs with relevant metadata.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS image_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_filename TEXT NOT NULL,
                    original_path TEXT NOT NULL,
                    mask_filename TEXT NOT NULL,
                    mask_path TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_size INTEGER,
                    image_width INTEGER,
                    image_height INTEGER
                )
            ''')
            
            conn.commit() # Commit changes to the database.
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()
    else:
        print("Error: Could not establish database connection")