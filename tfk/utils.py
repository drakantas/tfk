from asyncpg import Record
from typing import Union, Any

from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic.exceptions import InvalidUsage

from .errors import PayloadFieldsMethodMissing, MalformedJsonPayload, InvalidJsonPayload, NotCallable

DSN = 'postgres://{username}:{password}@{host}:{port}/{db}'


def parse_dsn(db_dict: dict) -> str:
    return DSN.format(username=db_dict['USER']['NAME'], password=db_dict['USER']['PASSWORD'], host=db_dict['HOST'],
                      port=db_dict['PORT'], db=db_dict['DATABASE_NAME'])


def get_model_name(cls):
    model_name = cls.__module__.split('.')[-2] + '_' + cls.__name__
    return model_name.lower()


def flatten_result(result: Union[list, tuple, Record]) -> Union[dict, list]:
    if isinstance(result, Record):
        return {k: v for k, v in result.items()}

    return [{k: v for k, v in record.items()} for record in result]


def check_payload(request: Request, view: HTTPMethodView, single_object: bool = True) -> Any:
    try:
        # Decoded json payload
        payload = request.json

        # Type of the attributes passed in the payload
        types = getattr(view, '_payload_fields')()
    except InvalidUsage:
        # The payload couldn't be parsed, therefore it isn't valid json
        raise MalformedJsonPayload
    except AttributeError:
        # The view class is missing the payload fields method
        raise PayloadFieldsMethodMissing
    except TypeError:
        # The payload fields method isn't a callable
        raise NotCallable('_payload_fields', view.__class__.__name__)

    # Type of payload
    if (single_object and not isinstance(payload, dict)) or (not single_object and not isinstance(payload, list)):
        raise InvalidJsonPayload

    # Amount of given fields to examine must match the amount of fields in the payload
    if len(types) != len(payload):
        raise InvalidJsonPayload

    # Type of each field in the payload
    for t in types.keys():
        if t in payload and isinstance(payload[t], types[t]):
            continue
        raise InvalidJsonPayload

    return payload
