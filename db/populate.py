#!/usr/bin/env python3

import csv
import sqlite3
import sys

INFILE =  sys.argv[1]
OUTFILE = sys.argv[2]

class Inventory:
    def __init__(self, path):
        self.rows = []
        with open(path) as invhandle:
            reader = csv.DictReader(invhandle)
            for row in reader:
                print(row)
                self.rows.append(Asset().from_inv(**row))
        self.len = len(self.rows)
        print(self.rows)
    
    def __iter__(self):
        self.counter = 0
        return self
    
    def __next__(self):
        if self.counter < self.len:
            current = self.rows[self.counter]
            self.counter += 1
            return current
        else:
            raise StopIteration
            

class Asset:
    def __init__(self):
        pass

    @classmethod
    def from_inv(self, **kwargs):
        self.dir     = kwargs.get('Directory')
        self.name    = kwargs.get('Filename')
        self.ext     = kwargs.get('Extension')
        self.bytes   = kwargs.get('Bytes')
        self.mtime   = kwargs.get('MTime')
        self.moddate = kwargs.get('Moddate')
        self.md5     = kwargs.get('MD5')

    @classmethod
    def from_database(self, id):
        pass

    def deposit_to(self, database):
        INSERT_CMD = '''INSERT INTO assets (
                            dir, name, ext, bytes, mtime, moddate, md5
                            )
                        VALUES ("{asset.dir}", 
                                "{asset.name}", 
                                "{asset.ext}",
                                 {asset.bytes},
                                 {asset.mtime},
                                "{asset.moddate}",
                                "{asset.md5}")'''
        database.execute(INSERT_CMD.format(asset=self))
                                

conn = sqlite3.connect(OUTFILE)
database = conn.cursor()
database.execute('''DROP TABLE IF EXISTS assets''')
database.execute('''CREATE TABLE assets(
                    id INTEGER PRIMARY KEY,
                    dir TEXT,
                    name TEXT,
                    ext TEXT,
                    bytes INTEGER,
                    mtime INTEGER,
                    moddate TEXT,
                    md5 TEXT)'''
                    )
inventory = Inventory(INFILE)
for asset in inventory:
    print(asset)
    asset.deposit_to(database)

database.execute('SELECT * FROM assets')
print(
    "Loaded {} rows into assets table".format(len(database.fetchall()))
    )
conn.commit()
conn.close()
