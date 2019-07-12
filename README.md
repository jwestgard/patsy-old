# PATSy
A preservation asset tracking system. This is a work in progress with two main parts:

1. A command-line interface to a SQLite database, and 
2. A Flask-based web interface.

The PATSy data model defines assets, instances, and manifests. *Assets* are blobs of data as defined by their checksums and size in bytes. Becuase this system is focused on preservation, assets are treated as immutable. *Instances* are copies of assets stored in some location (e.g. a server, tape backup, or portable HDD).  *Manifests* are list of instances of assets, basically records of the files stored in a particular location at the time the manifest was made.
