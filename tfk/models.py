from typing import Union, Tuple
from datetime import datetime

from .utils import get_model_name, flatten_result
from .errors import NonexistentModel, OverlappingModel


class Models(dict):
    def __getattr__(self, model: str):
        if model not in self:
            raise NonexistentModel("Model {model} not found.".format(model=model))

        return self[model]

    def __setattr__(self, model, instance):
        if model in self:
            raise OverlappingModel("Attempted to overlap model {model}. Object instance at {instance}.".format(
                model=model, instance=hex(id(instance))))

        self[model] = instance

    def remove(self, model):
        if model not in self:
            raise NonexistentModel("Couldn't delete model {model}, it wasn't be found.".format(model=model))

        del self[model]


class Model:
    def __init__(self, *args):
        self.pool = args[0]
        self.db_config = args[1]
        self._table_name = self.set_table_name()

    @classmethod
    def set_table_name(cls):
        return cls.__dict__['TABLE_NAME'] if 'TABLE_NAME' in cls.__dict__ else None or get_model_name(cls)

    @staticmethod
    def timestamps() -> Tuple[datetime, datetime]:
        return datetime.utcnow(), datetime.utcnow()

    async def fetch(self, query: str, args: Union[list, tuple] = list(), single: bool = False, flatten: bool = False):
        _method = 'fetch' if not single else 'fetchrow'
        query = self.format_statement(query)

        async with self.pool.acquire() as connection:
            statement = await connection.prepare(query)
            results = await getattr(statement, _method)(*args)

            return flatten_result(results) if flatten and results else results

    async def execute(self, update_query: str, args: Union[list, tuple] = list()):
        update_query = self.format_statement(update_query)

        async with self.pool.acquire() as connection:
            return await connection.execute(update_query, *args)

    def format_statement(self, statement):
        return statement.format(table=self._table_name, schema=self.db_config['SCHEMA'] + '.')
