# db_setup.py
import sqlite3

def create_tables(db_name="companies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            primary_link TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secondary_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            secondary_link TEXT,
            FOREIGN KEY (company_id) REFERENCES companies (id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created.")
