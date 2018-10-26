import sqlite3


class Connection():

    def __init__(self):
        conn = sqlite3.connect(OUTFILE)
        cursor = conn.cursor()



    def check_db(self, cursor):
        query = (
            f'SELECT * FROM batches'
            f'WHERE md5="{self.md5}" and bytes="{self.bytes}"'
            )
        cursor.execute 
