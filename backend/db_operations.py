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

def get_image_pair(pair_id):
    """
    Retrieve an image pair from the database
    
    Args:
        pair_id (int): ID of the image pair
    
    Returns:
        dict: Image pair information
    """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM image_pairs WHERE id = ?", (pair_id,)) # Query to find the image pair by ID.
            row = cursor.fetchone() # Fetch one record from the result set.
            
            if row: # Check if a record was found.
                return {
                    'id': row[0],
                    'original_filename': row[1],
                    'original_path': row[2],
                    'mask_filename': row[3],
                    'mask_path': row[4],
                    'upload_date': row[5],
                    'file_size': row[6],
                    'width': row[7],
                    'height': row[8]
                } # Return the image pair information as a dictionary.
            return None # Return None if no record was found.
        except Error as e:
            print(f"Error retrieving image pair: {e}")
            return None
        finally:
            conn.close()
    return None

def get_recent_image_pairs(limit=10):
    """
    Get most recently uploaded image pairs
    
    Args:
        limit (int): Maximum number of pairs to retrieve
    
    Returns:
        list: List of image pairs
    """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM image_pairs ORDER BY upload_date DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            return [{
                'id': row[0],
                'original_filename': row[1],
                'original_path': row[2],
                'mask_filename': row[3],
                'mask_path': row[4],
                'upload_date': row[5],
                'file_size': row[6],
                'width': row[7],
                'height': row[8]
            } for row in rows]
        except Error as e:
            print(f"Error retrieving recent image pairs: {e}")
            return []
        finally:
            conn.close()
    return []