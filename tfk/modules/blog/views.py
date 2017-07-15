from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import json

from ...utils import check_payload


def gen_slug(title: str) -> str:
    return ''


class Entries(HTTPMethodView):
    async def get(self, request: Request):
        model = request.app.models.blog_entry

        entries = await model.get_chunk(5)

        return json(entries)


class Single(HTTPMethodView):
    async def get(self, request: Request, slug: str):
        model = request.app.models.blog_entry

        entry = await model.get_single(slug)

        return json(entry)


class CreateEntry(HTTPMethodView):
    async def post(self, request: Request):
        # Data for the new entry
        payload = check_payload(request, self)

        return json(payload, status=200)

    @staticmethod
    def _payload_fields():
        return {
            't': str,
            'b': str
        }
