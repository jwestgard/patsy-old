import csv
import pytest

from argparse import Namespace
from patsy.commands.schema import Command
from patsy.commands.load import Command as LoadCommand
from patsy.core.db_gateway import DbGateway
from patsy.core.patsy_record import PatsyUtils
from patsy.model import Base
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles


# pytestmark = pytest.mark.parametrize(
#     "addr", [":memory"]  # , "postgresql+psycopg2://postgres:password@localhost:5432/postgres"]
# )

@pytest.fixture
def addr(request):
    return request.config.getoption('--base-url')


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def setUp(obj, addr):
    test_db_files = [
        "tests/fixtures/db_gateway/colors_inventory.csv",
        "tests/fixtures/db_gateway/solar_system_inventory.csv"
    ]

    args = Namespace()
    args.database = addr
    obj.gateway = DbGateway(args)
    # schema = Schema(obj.gateway)
    # schema.create_schema()
    Command.__call__(obj, args, obj.gateway)
    for file in test_db_files:
        args.file = file
        LoadCommand.__call__(obj, args, obj.gateway)
        # load = Load(obj.gateway)
        # load.process_file(file)


def tearDown(obj):
    obj.gateway.close()
    Base.metadata.drop_all(obj.gateway.session.get_bind())


class TestDbGateway:
    def test_get_all_batches(self, addr):
        try:
            setUp(self, addr)
            batches = self.gateway.get_all_batches()
            assert len(batches) == 2
            batch_names = [batch.name for batch in batches]
            assert "TEST_COLORS" in batch_names
            assert "TEST_SOLAR_SYSTEM" in batch_names
        finally:
            tearDown(self)

    def test_get_batch_by_name__batch_does_not_exist(self, addr):
        try:
            setUp(self, addr)
            batch = self.gateway.get_batch_by_name("NON_EXISTENT_BATCH")
            assert batch is None
        finally:
            tearDown(self)

    def test_get_batch_by_name__batch_exists(self, addr):
        try:
            setUp(self, addr)
            batch = self.gateway.get_batch_by_name("TEST_COLORS")
            assert batch is not None
            assert batch.name == "TEST_COLORS"
        finally:
            tearDown(self)

    def test_get_batch_records__batch_does_not_exist(self, addr):
        try:
            setUp(self, addr)
            patsy_records = self.gateway.get_batch_records("NON_EXISTENT_BATCH")
            assert len(patsy_records) == 0
        finally:
            tearDown(self)

    def test_get_batch_records__batch_exists(self, addr):
        try:
            setUp(self, addr)
            patsy_records = self.gateway.get_batch_records("TEST_COLORS")
            expected_patsy_records = []
            expected_csv = []
            with open("tests/fixtures/db_gateway/colors_inventory.csv") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    row_record = PatsyUtils.from_inventory_csv(row)
                    expected_patsy_records.append(row_record)
                    expected_csv.append(PatsyUtils.to_csv(row_record))

            assert len(expected_patsy_records) >= 0
            assert len(expected_patsy_records) == len(patsy_records)

            for p in patsy_records:
                record_csv = PatsyUtils.to_csv(p)
                assert p in expected_patsy_records
                assert record_csv in expected_csv

        finally:
            tearDown(self)
