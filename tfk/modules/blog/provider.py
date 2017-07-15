from sanic import Sanic, Blueprint

from . import models, views


async def __models__():
    return models.Entry,


async def register(app: Sanic, rest_api: Blueprint):
    await register_routes(rest_api)


async def register_routes(rest_api: Blueprint):
    # Fetch latest chunk of blog entries.
    rest_api.add_route(views.Entries.as_view(), '/blog/entries')

    # Fetch a single blog entry.
    rest_api.add_route(views.Single.as_view(), '/blog/read/<slug:[a-zA-Z0-9\-]+>')

    # Create a blog entry.
    rest_api.add_route(views.CreateEntry.as_view(), '/blog/entries')
