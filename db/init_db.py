#!/usr/bin/env python3

import os
import sqlite3
import sys
import yaml

header = '| PATSy database initialization |'
border = '-' * len(header)
print('\n'.join([border, header, border]))

configfile = os.path.abspath(sys.argv[1])
rootdir = os.path.split(configfile)[0]

print('Reading configuration from {0}...'.format(configfile))

with open(configfile) as handle:
    config = yaml.safe_load(handle)

dbpath = os.path.normpath(os.path.join(rootdir, config['DB_FILE']))
schema = os.path.normpath(os.path.join(rootdir, config['DB_SCHEMA']))

print('Initializing database at {0}...'.format(dbpath))

con = sqlite3.connect(dbpath)
cur = con.cursor()
with open(schema) as handle:
    cur.executescript(handle.read())
result = cur.execute('''SELECT name FROM sqlite_master WHERE 
                        type='table';''').fetchall()

print('Successfully initialized database with {0} tables.'.format(len(result)))

con.commit()
con.close()
