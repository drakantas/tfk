import ujson as json

from asyncpg import create_pool
from asyncio import AbstractEventLoop
from inspect import iscoroutinefunction

from sanic import Sanic, Blueprint

from .errors import ConfigException
from .models import Models
from .utils import parse_dsn, get_model_name

from .modules import blog, auth

providers = (
    blog.provider,
    auth.provider
)


def bootstrap() -> Sanic:
    try:
        with open('tfk/config/app.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        raise ConfigException("The main configuration file, app.json, couldn't be found.")
    except ValueError:
        raise ConfigException('Unable to parse the contents of app.json.')
    else:
        if 'DB' not in config:
            raise ConfigException("Couldn't find the database configuration keys.")
        elif not isinstance(config['DB'], dict):
            raise ConfigException('The database configuration must be stored as a json object.')

    # Create an instance of the app.
    app = Sanic(config['NAME'])

    # Update the configuration dict.
    app.config.update(config)

    # REST API Blueprint
    rest_api = Blueprint('REST API', url_prefix='/api')

    @app.listener('before_server_start')
    async def setup_db(_app: Sanic, loop: AbstractEventLoop):
        # Attach database connection pool to the application.
        _app.db = await create_pool(parse_dsn(_app.config.DB))

        # Create models dict within the application.
        _app.models = Models()

        def init_model(_callable, pool=_app.db, db_config=_app.config.DB):
            model_name = get_model_name(_callable)
            setattr(_app.models, model_name, _callable(pool, db_config))

        def register_models(models):
            if not models:
                return

            for model in models:
                init_model(model)

        async def run_func(obj, func_name: str, *args, deco=None):
            func = getattr(obj, func_name)

            if iscoroutinefunction(func):
                func = await func(*args)
            else:
                func = func(*args)

            if callable(deco):
                return deco(func)
            return func

        for provider in providers:
            await run_func(provider, '__models__', deco=(lambda _models: register_models(_models)))
            await run_func(provider, 'register', _app, rest_api)

        # And lastly, we register the blueprint for the REST API
        _app.blueprint(rest_api)

    return app
