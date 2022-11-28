from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.orm import sessionmaker

from datakenobi.db.base import (
    ConnectionBuilder,
    ConnectionData,
    Connector,
    SqlAlchemyConnector,
)


def test_connector():
    """Testa BaseConnector."""
    connector = Connector()
    assert connector.engine is None
    assert connector.connection is None


def test_sqlalchemy_conector_create_engine():
    url = "sqlite:///test.db"
    sac = SqlAlchemyConnector(url=url)
    sac.create_engine()
    assert isinstance(sac.engine, Engine)


def test_sqlalchemy_conector_create_connection():
    url = "sqlite:///test.db"
    sac = SqlAlchemyConnector(url=url)
    sac.create_engine()
    sac.create_conn()
    assert isinstance(sac.connection, Connection)


def test_sqlalchemy_conector_session():
    url = "sqlite:///test.db"
    sac = SqlAlchemyConnector(url=url)
    sac.create_engine()
    assert isinstance(sac.session, sessionmaker)


def test_connection_builder():
    connection_data = ConnectionData()
    connection_data.drivername = "mssql+pyodbc"
    connection_data.host = "localhost"
    connection_data.database = "test"
    connection_data.username = "username"
    connection_data.password = "password"
    connection_data.query = {"Trusted_Connection": "yes"}

    conn_builder = ConnectionBuilder(SqlAlchemyConnector, connection_data)
    connector = conn_builder.build()
    assert isinstance(connector, SqlAlchemyConnector)
