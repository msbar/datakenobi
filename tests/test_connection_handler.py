from datakenobi.db.connection_handler import ConnectionHandler


def test_connection_handler_url():
    ch = ConnectionHandler(alias="default")
    ch.connector


def test_connection_handler():
    ch = ConnectionHandler(alias="test")
    ch.connector


def test_connection_handler():
    ch = ConnectionHandler(alias="test_crypton")
    ch.connector
