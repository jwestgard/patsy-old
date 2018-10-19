DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS batches;
DROP TABLE IF EXISTS instances;

CREATE TABLE assets(    
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    bytes    INTEGER,
    md5      TEXT,
    sha1     TEXT,
    sha256   TEXT
    );

CREATE TABLE batches(   
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    filename TEXT,
    number   INTEGER,
    date     TEXT
    );

CREATE TABLE instances( 
    id       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    filename TEXT,
    path     TEXT,
    location TEXT,
    created  TEXT,
    batch_id INTEGER,
    asset_id INTEGER
    );
