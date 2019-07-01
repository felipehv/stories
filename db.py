import sqlite3 as db

"""
    Images Schema
uniqueID: text      -   uniqueID
partNumber: text    -   partNumber
name: text          -   name
image: text url     -   fullImage
listprice: int      -   prices.listPrice
offerprice: int     -   prices.offerPrice
url: text url *     -   url
type: text          -   (top,bottom,full)
"""

class Database():

    def __init__(self):
        self.conn = db.connect("clothes.db")
        self.cursor = self.conn.cursor()

    def setup(self):
        self.cursor.execute("""
        CREATE TABLE clothes( 
                partNumber text primary key,
                name text,
                image text,
                listprice int,
                offerprice int,
                url text,
                type text,
                gender text
            );
        """)
        self.conn.commit()

    def get_clients(self):
        self.cursor.execute("SELECT client_id, folder_id FROM clients;")
        clients = self.cursor.fetchall()
        cursor2 = self.conn.cursor()


    def reset(self):
        self.cursor.execute("DROP TABLE IF EXISTS clothes;")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_all_clothes(self):
        return self.cursor.execute("SELECT * FROM clothes;")

if __name__ == "__main__":
    db = Database()
    db.fix_img_url()
    db.close()