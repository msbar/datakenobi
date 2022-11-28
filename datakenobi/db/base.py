from crypton_tool.crypton import Crypton
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from settings import CRYPTON_TOKEN_PATH, DATABASES


class Connector:
    def __init__(
        self,
        drivername=None,
        host=None,
        database=None,
        username=None,
        password=None,
        query=None,
        url=None,
        *args,
        **kwargs,
    ):
        self._drivername = drivername
        self._host = host
        self._database = database
        self._username = username
        self._password = password
        self._query = query
        self._url = url
        self._engine = None
        self._connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def create_engine(self):
        pass

    @property
    def engine(self):
        return self._engine

    def create_conn(self):
        pass

    @property
    def connection(self):
        return self._connection

    def close(self):
        pass


class SqlAlchemyConnector(Connector):
    def __repr__(self):
        return f"{__class__}(host={self._host}, database={self._database})"

    def __str__(self):
        return f"{__class__}(host={self._host}, database={self._database})"

    def create_engine(self):
        if not self._url:
            self._url = URL.create(
                drivername=self._drivername,
                host=self._host,
                database=self._database,
                username=self._username,
                password=self._password,
                query=self._query,
            )
        self._engine = create_engine(self._url)
        return self._engine

    def create_conn(self):
        self._connection = self._engine.connect()
        return self._connection

    @property
    def session(self):
        return sessionmaker(self._engine)

    def close(self):
        self._connection.close()
        self._engine.dispose()


class ConnectionData:
    def __init__(self) -> None:
        self._drivername = None
        self._host = None
        self._database = None
        self._username = None
        self._password = None
        self._query = None
        self._url = None

    @property
    def drivername(self):
        return self._drivername

    @drivername.setter
    def drivername(self, drivername):
        self._drivername = drivername

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def get_data(self):
        return {
            "drivername": self._drivername,
            "host": self._host,
            "database": self._database,
            "username": self._username,
            "password": self._password,
            "query": self._query,
            "url": self._url,
        }


class ConnectionBuilder:
    def __init__(self, connector, connection_data) -> None:
        self._connector = connector
        self._connection_data = connection_data
        self.__connector_instance = None

    @property
    def connector(self):
        return self._connector

    @property
    def connection_data(self):
        return self._connection_data

    @property
    def connector_instance(self):
        return self.__connector_instance

    def build(self):
        self.__connector_instance = self._connector(**self._connection_data.get_data)
        return self.__connector_instance


class ReadConnectionDataConf:
    def __init__(self, alias) -> None:
        self._alias = alias
        self._connection_data = ConnectionData()
        self._conf_database = DATABASES.get(alias)

    def get_credentials(self):
        username = self._conf_database.get("USERNAME", None)
        password = self._conf_database.get("PASSWORD", None)

        if self._conf_database.get("CRYPTON", None):
            token = Crypton.read_token_file(CRYPTON_TOKEN_PATH)
            crypton = Crypton(token)

            username = crypton.decrypt_content(username)
            password = crypton.decrypt_content(password)

        return (username, password)

    def get_conf(self):
        username, password = self.get_credentials()
        self._connection_data.drivername = self._conf_database.get("DRIVERNAME", None)
        self._connection_data.host = self._conf_database.get("HOST", None)
        self._connection_data.database = self._conf_database.get("DATABASE", None)
        self._connection_data.username = username
        self._connection_data.password = password
        self._connection_data.query = self._conf_database.get("QUERY", None)
        self._connection_data.url = self._conf_database.get("URL", None)

        return self._connection_data
