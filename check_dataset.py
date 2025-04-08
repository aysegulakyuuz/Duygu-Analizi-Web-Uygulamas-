import sqlite3

# Veritabanına bağlan
conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()

# Verileri sorgula
cursor.execute("SELECT * FROM feedback")
rows = cursor.fetchall()


if rows:
    print("Saved Feedback:")
    for row in rows:
       print(f"\n\n   ID: {row[0]}, Metin: {row[1]}, Algılanan Duygu: {row[2]}, Gerçek Duygu: {row[3]}, Doğru Mu?: {row[4]}   \n\n")

else:
    print("There are no records in the database yet.")


conn.close()
