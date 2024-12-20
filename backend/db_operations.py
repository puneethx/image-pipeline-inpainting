from datetime import datetime
from sqlite3 import Error
from db_config import create_connection

def insert_image_pair(original_info, mask_info):
    """
    Insert a new image pair into the database
    
    Args:
        original_info (dict): Original image information
        mask_info (dict): Mask image information
    
    Returns:
        int: The ID of the newly inserted record, or None if the insertion failed.
    """
    conn = create_connection() # Establish a connection to the database.
    if conn is not None:
        try:
            cursor = conn.cursor() # Create a cursor object for executing SQL commands.
            sql = '''INSERT INTO image_pairs
                     (original_filename, original_path, mask_filename, mask_path,
                      file_size, image_width, image_height)
                     VALUES (?, ?, ?, ?, ?, ?, ?)'''
            
            # Prepare values for the SQL statement from the provided dictionaries.
            values = (
                original_info['filename'],
                original_info['path'],
                mask_info['filename'],
                mask_info['path'],
                original_info.get('file_size'),
                original_info.get('width'),
                original_info.get('height')
            )
            
            cursor.execute(sql, values)
            conn.commit() # Commit the transaction to save changes to the database.
            return cursor.lastrowid # Return the ID of the newly inserted record.
        except Error as e:
            print(f"Error inserting image pair: {e}")
            return None
        finally:
            conn.close()
    return None

def get_recent_image_pairs(limit=10):
    """
    Fetch the most recent image pairs from the database.
    Args:
        limit (int): Number of recent pairs to fetch.
    Returns:
        list: A list of image pair dictionaries.
    """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = f'''
                SELECT 
                    id, original_filename, original_path, 
                    mask_filename, mask_path, upload_date
                FROM image_pairs
                ORDER BY upload_date DESC
                LIMIT ?
            '''
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()

            # Convert rows to a list of dictionaries.
            image_pairs = [
                {
                    "id": row[0],
                    "original_filename": row[1],
                    "original_path": row[2],
                    "mask_filename": row[3],
                    "mask_path": row[4],
                    "upload_date": row[5]
                }
                for row in rows
            ]

            return image_pairs
        except Error as e:
            print(f"Error fetching image pairs: {e}")
            return []
        finally:
            conn.close()
    return []
