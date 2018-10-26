import hashlib
import os
from datetime import datetime as dt


def calculate_hash(path, alg):
    '''Given a path to a file and a hash algorithm, calculate and 
       return the hash digest of the file'''
    hash = getattr(hashlib, alg)()
    with open(path, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            else:
                hash.update(data)
        return hash.hexdigest()


class Inventory():
    '''Object representing a text file containing metadata 
       about preserved assets.'''


    @classmethod
    def from_database(cls):
        pass


    @classmethod
    def from_file(cls, path):
        abspath = os.path.abspath(path)
        mtime = os.path.getmtime(abspath)
        kwargs = {
            'filename': os.path.basename(abspath),
            'md5': calculate_hash(abspath, 'md5'),
            'mtime': int(mtime),
            'bytes': os.path.getsize(abspath),
            'ext': os.path.splitext(abspath)[1].lstrip('.').upper(),
            'moddate': dt.fromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%S')
            }
        return cls(**kwargs)

    def __init__(self, **kwargs):
        attribs = ['filename', 
                   'md5', 
                   'sha1', 
                   'sha256', 
                   'mtime', 
                   'bytes'
                   'ext', 
                   'moddate'
                   ]

        for attrib in attribs:
            value = kwargs.get(attrib, None)
            setattr(self, attrib, value)

