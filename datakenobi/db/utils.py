import logging
from pathlib import Path

from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateIndex, CreateTable


def get_sql_file(file_path: Path):
    return Path(file_path).read_text()


class CreateModelTable:
    def __init__(self) -> None:
        self._log = logging.getLogger(f"{__class__}")

    def create_all(self, engine):
        from sqlalchemy.ext.declarative import declarative_base

        try:
            Base = declarative_base()
            Base.metadata.create_all(engine)
        except Exception as e:
            self._log.exception(e)
            raise e
        else:
            self._log.info("Tabelas criadas.")
            return True

    def create_table_from_model(self, engine, model):
        try:
            model.metadata.create_all(engine)
        except Exception as e:
            self._log.exception(e)
            raise e
        else:
            self._log.info("Tabela criada.")
            return True


class CreateModelTempTable:
    def __init__(self, engine) -> None:
        self._engine = engine
        self._log = logging.getLogger(f"{__class__}")

    def create_table_temp(self, model):
        try:
            table_name = model.__tablename__
            table_name_temp = f"{model.__tablename__}_temp"
            create_stmt1 = CreateTable(model.__table__).compile(self._engine).__str__()
            create_stmt1 = create_stmt1.replace(table_name, table_name_temp)
            create_stmt1 = text(create_stmt1)

            stm_index_list = []
            if model.__table__.indexes:
                for index in model.__table__.indexes:
                    stm = CreateIndex(index).compile(self._engine).__str__()
                    stm_index_list.append(stm)

                create_stmt2 = ";".join(stm_index_list)
                create_stmt2 = create_stmt2.replace(table_name, table_name_temp)
                create_stmt2 = text(create_stmt2)

            self._engine.execute(create_stmt1)
            if model.__table__.indexes:
                self._engine.execute(create_stmt2)
        except Exception as e:
            self._log.exception(e)
            raise e
        else:
            self._log.info("Tabela temporária criada.")
            return True


class RenameTable:
    def __init__(self, engine) -> None:
        self.engine = engine
        self._log = logging.getLogger(f"{__class__}")

    def rename_table_sqlserver(self, old_table_name, new_table_name, schema=None):
        self._query = text(
            f"EXEC sp_rename '{schema}.{old_table_name}', '{new_table_name}';"
        )
        self.rename_exec()

    def rename_table(self, old_table_name, new_table_name, schema=None):
        self._query = text(
            f"ALTER TABLE {schema}.{old_table_name} RENAME TO {new_table_name};"
        )
        self.rename_exec()

    def rename_exec(self):
        with self.engine.connect() as connection:
            with connection.begin():
                try:
                    connection.execute(self._query)
                except Exception as e:
                    self._log.exception(e)
                    raise e
                else:
                    self._log.info("Tabela renomeada.")
                    return True


class DropTableFromRawSql:
    def __init__(self, engine) -> None:
        self.engine = engine
        self._log = logging.getLogger(f"{__class__}")

    def drop(self, table_name, schema=None):
        query = text(f"DROP TABLE [{schema}].[{table_name}]")
        try:
            self.engine.execute(query)
        except Exception as e:
            self._log.exception(e)
            raise e
        else:
            self._log.info("Tabela renomeada.")
            return True


class DropTableSqlAlchemy:
    def __init__(self, engine) -> None:
        self._engine = engine
        self._log = logging.getLogger(f"{__class__}")

    def drop(self, model):
        try:
            model.__table__.drop(self._engine)
        except Exception as e:
            self._log.exception(e)
            raise e
        else:
            self._log.info("Tabela apagada.")
            return True


class HasTable:
    def __init__(self, engine) -> None:
        self._log = logging.getLogger(f"{__class__}")
        self._engine = engine
        self._inspect = inspect(self._engine)

    def has_table(self, table_name, schema=None):
        return self._inspect.has_table(table_name, schema)

    def has_table_from_model(self, model):
        return self._inspect.has_table(
            model.__tablename__, model.__table_args__["schema"]
        )
