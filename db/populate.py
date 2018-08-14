#!/usr/bin/env python3

import csv
import sqlite3
import sys

INSERT_CMD = '''INSERT INTO assets (dir, name, ext, bytes, 
                                    mtime, moddate, md5)
                VALUES ("{asset.dir}", "{asset.name}", "{asset.ext}",
                         {asset.bytes}, {asset.mtime}, "{asset.moddate}",
                         "{asset.md5}")'''
INFILE =  sys.argv[1]
OUTFILE = sys.argv[2]

class Asset:
    def __init__(self, Directory, Filename, Extension, Bytes, MTime, 
                 Moddate, MD5):
        self.dir     = Directory
        self.name    = Filename
        self.ext     = Extension
        self.bytes   = Bytes
        self.mtime   = MTime
        self.moddate = Moddate
        self.md5     = MD5

conn = sqlite3.connect(OUTFILE)
cursor = conn.cursor()
cursor.execute('''DROP TABLE IF EXISTS assets''')
cursor.execute('''CREATE TABLE assets(
                    id INTEGER PRIMARY KEY,
                    dir TEXT,
                    name TEXT,
                    ext TEXT,
                    bytes INTEGER,
                    mtime INTEGER,
                    moddate TEXT,
                    md5 TEXT)'''
                    )

with open(INFILE) as inputfile:
    reader = csv.DictReader(inputfile, delimiter=',')
    for d in reader:
        a = Asset(**d)
        cursor.execute(INSERT_CMD.format(asset=a))

cursor.execute('SELECT * FROM assets')
print(
    "Loaded {} rows into assets table".format(len(cursor.fetchall()))
    )

conn.commit()
conn.close()
