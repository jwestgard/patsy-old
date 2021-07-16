from argparse import Namespace
from sqlalchemy.exc import IntegrityError
from patsy.database import Session
from patsy.core.patsy_record import PatsyRecord
from patsy.model import Batch, Accession, Location
from patsy.database import use_database_file
from typing import Dict, Optional


class AddResult():
    def __init__(self) -> None:
        self.batches_added = 0
        self.accessions_added = 0
        self.locations_added = 0


class DbGateway():
    def __init__(self, args: Namespace) -> None:
        use_database_file(args.database)
        self.session = Session()
        self.batch_ids: Dict[str, int] = {}

    def add(self, patsy_record: PatsyRecord) -> AddResult:
        self.add_result = AddResult()
        batch_name = patsy_record.batch
        batch_id = self.batch_ids.get(batch_name, None)

        if batch_id is None:
            batch = self.find_or_create_batch(patsy_record)
            batch_id = batch.id
            self.batch_ids[batch_name] = batch_id

        accession = self.find_or_create_accession(batch_id, patsy_record)
        location = self.find_or_create_location(patsy_record)
        if location:
            accession.locations.append(location)
        return self.add_result

    def find_or_create_batch(self, patsy_record: PatsyRecord) -> Batch:
        batch_name = patsy_record.batch
        batch: Batch = self.session.query(Batch).filter(Batch.name == batch_name).first()

        if batch is None:
            batch = Batch(name=batch_name)
            self.session.add(batch)
            self.session.commit()
            self.add_result.batches_added += 1

        return batch

    def find_or_create_accession(self, batch_id: int, patsy_record: PatsyRecord) -> Accession:
        accession: Accession = self.session.query(Accession).filter(
            Accession.batch_id == batch_id,
            Accession.relpath == patsy_record.relpath
        ).first()

        if accession is None:
            accession = Accession(
                relpath=patsy_record.relpath,
                filename=patsy_record.filename,
                extension=patsy_record.extension,
                bytes=patsy_record.bytes,
                timestamp=patsy_record.moddate,
                md5=patsy_record.md5,
                sha1=patsy_record.sha1,
                sha256=patsy_record.sha256
            )
            accession.batch_id = batch_id
            self.session.add(accession)
            self.add_result.accessions_added += 1

        return accession

    def find_or_create_location(self, patsy_record: PatsyRecord) -> Optional[Location]:
        storage_location = patsy_record.storage_location
        if not storage_location:
            return None

        location: Location = self.session.query(Location).filter(
            Location.storage_location == patsy_record.storage_location,
            Location.storage_provider == patsy_record.storage_provider
        ).first()

        if location is None:
            location = Location(
                storage_location=patsy_record.storage_location,
                storage_provider=patsy_record.storage_provider
            )
            self.session.add(location)
            self.add_result.locations_added += 1

        return location

    def close(self) -> None:
        try:
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()