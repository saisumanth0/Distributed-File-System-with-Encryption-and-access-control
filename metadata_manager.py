import sqlite3
import os

# Initialize SQLite database for metadata
def init_metadata_db():
    # Define the database file location
    db_path = "metadata/metadata.db"

    # Create metadata directory if it doesn't exist
    os.makedirs("metadata", exist_ok=True)

    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table for storing file metadata (e.g., file name, storage node, encryption status)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            storage_node TEXT NOT NULL,
            encrypted INTEGER NOT NULL,
            permissions TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

    print("Metadata database initialized.")

# Call the function to initialize the database
if __name__ == "__main__":
    init_metadata_db()
