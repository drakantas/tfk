from sanic import Sanic, Blueprint

from . import models, views


async def __models__():
    return models.User, models.Authenticable


async def register(app: Sanic, rest_api: Blueprint):
    await register_routes(rest_api)


async def register_routes(rest_api: Blueprint):
    rest_api.add_route(views.RegisterUser.as_view(), '/auth/register')

    rest_api.add_route(views.Login.as_view(), '/auth/login')
