import sqlite3 as sql
from msvcrt import getch

def main():
    with sql.connect("sample.db") as connection:
        cur = connection.cursor()
        try:
            cur.execute("DROP TABLE posts")
        except:
            pass
        cur.execute('CREATE TABLE posts(title TEXT, description TEXT)')
        cur.execute('INSERT INTO posts VALUES ("Good", "so good !")')    
        cur.execute('INSERT INTO posts VALUES ("Well", "so well !")')

try:
    main()
except Exception as e:
    print("Error:", e)

getch()