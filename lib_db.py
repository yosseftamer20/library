import sqlite3
conn = sqlite3.connect(r'C:\Users\yosse\PycharmProjects\pythonProject1\library system\db')
c = conn.cursor()
id1= input("enter id")
c.execute(f"SELECT * FROM books where id = {id1}")
rows = c.fetchall()
for row in rows:
    print(row)
c.close()
conn.close()