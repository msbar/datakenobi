from datakenobi.db.utils import (
    ConnectionBuilder,
    ReadConnectionDataConf,
    SqlAlchemyConnector,
)


class ConnectionHandler:
    def __init__(self, alias="default"):
        self._alias = alias
        self._connector = None

    @property
    def connector(self):
        rcd = ReadConnectionDataConf(self._alias)
        self._connector = ConnectionBuilder(
            connector=SqlAlchemyConnector, connection_data=rcd.get_conf()
        ).build()
        return self._connector
