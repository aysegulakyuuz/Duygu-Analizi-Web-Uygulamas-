import sqlite3

def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            detected_emotion TEXT NOT NULL,
            actual_emotion TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("The database was created successfully.")

if __name__ == '__main__':
    init_db()
