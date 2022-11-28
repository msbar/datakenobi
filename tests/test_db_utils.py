from datakenobi.db.connection_handler import ConnectionHandler
from datakenobi.db.utils import (
    CreateModelTable,
    CreateModelTempTable,
    DropTableFromRawSql,
    DropTableSqlAlchemy,
    HasTable,
    RenameTable,
)
from tests.models.car_model import Car

db = ConnectionHandler().connector
engine = db.create_engine()


def test_create_table_from_model():
    cmt = CreateModelTable()
    cmt.create_table_from_model(engine=engine, model=Car)

    hs = HasTable(engine=engine)
    assert hs.has_table_from_model(Car)


def test_create_table_temp_from_model():
    cmt = CreateModelTempTable(engine=engine)
    cmt.create_table_temp(model=Car)

    hs = HasTable(engine=engine)
    assert hs.has_table("Car_temp", schema="main")

    dts = DropTableFromRawSql(engine=engine)
    dts.drop(table_name="Car_temp", schema="main")


def test_drop_table_sqlalchemy():
    dts = DropTableSqlAlchemy(engine=engine)
    dts.drop(model=Car)

    hs = HasTable(engine=engine)
    assert not hs.has_table_from_model(Car)


def test_rename_table():
    OLD_TABLENAME = "Car"
    SCHEMA = "main"
    NEW_TABLENAME = "Cars"

    cmt = CreateModelTable()
    cmt.create_table_from_model(engine=engine, model=Car)

    rt = RenameTable(engine=engine)
    rt.rename_table(
        old_table_name=OLD_TABLENAME, new_table_name=NEW_TABLENAME, schema=SCHEMA
    )

    hs = HasTable(engine=engine)
    assert hs.has_table(table_name=NEW_TABLENAME, schema=SCHEMA)

    dts = DropTableFromRawSql(engine=engine)
    dts.drop(table_name=NEW_TABLENAME, schema=SCHEMA)
