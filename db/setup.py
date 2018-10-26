import sqlite3
import sys

with open(sys.argv[1]) as handle:
    setupscript = handle.read()

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript(setupscript)
