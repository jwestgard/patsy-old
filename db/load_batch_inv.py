#!/usr/bin/env python3

import csv
import os
import sqlite3
import sys

INVENTORY = sys.argv[1]
DATABASE  = sys.argv[2]


class Batch:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = filepath.split('/')[-1]
        self.date = os.path.getmtime(filepath)

    def create_db_entry(self, cursor):
        query =  '''
            INSERT INTO batches (filename, date) 
                VALUES ("{filename}", "{date}")
                '''.format(**self.__dict__)
        cursor.execute(query)
        self.id = cursor.lastrowid


class CSV_row:
    def __init__(self, batch, data):
        self.batch = batch.filename
        for k, v in data.items():
            setattr(self, k.lower(), v)
            print(k,v)

    def create_asset(self, cursor):
        query =  '''
            INSERT INTO assets (filename, ext, bytes, mtime, date, md5)
                VALUES ("{filename}", "{extension}", {bytes}, {mtime},
                "{moddate}", "{md5}")
                '''.format(**self.__dict__)
        cursor.execute(query)

    def check_for_asset(self, cursor):
        query = '''
            SELECT * FROM assets WHERE md5 = "{md5}" and bytes = "{bytes}"
            '''.format(**self.__dict__)
        return cursor.execute(query)

    def create_instance(self, cursor, batch_id, asset_id):
        query =  '''
            INSERT INTO instances (filename, batch_id, asset_id)
                VALUES ("{0}", {1}, {2})
                '''.format(self.filename, batch_id, asset_id)
        cursor.execute(query)


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

inventory = Batch(INVENTORY)
inventory.create_db_entry(cursor)
with open(inventory.filepath, 'r') as filehandle:
    reader = csv.DictReader(filehandle)
    for row in reader:
        entry = CSV_row(inventory, row)
        existing = entry.check_for_asset(cursor)
        if existing is None:
            entry.create_asset(cursor)
        entry.create_instance(cursor, inventory.id, cursor.lastrowid)

conn.commit()
conn.close()
