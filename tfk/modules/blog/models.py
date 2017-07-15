from datetime import datetime

from ...models import Model


class Entry(Model):
    async def get_chunk(self, chunk: int, offset: int = 0):
        """
        Fetch blog entries by chunks whilst also offsetting a given amount of entries.

        :param chunk:
        :param offset:
        :return:
        """
        q = 'SELECT postable.id, {table}.title, {table}.slug, {table}.author_id, {table}.body, postable.created_at, ' \
            'postable.updated_at FROM {schema}{table} INNER JOIN {schema}postable ON {table}.id = postable.id ORDER ' \
            'BY postable.created_at DESC LIMIT $1 OFFSET $2'

        return await self.fetch(q, args=(chunk, offset), flatten=True)

    async def get_single(self, slug: str):
        """
        Fetch a single blog entry.

        :param slug:
        :return:
        """
        q = 'SELECT postable.id, {table}.title, {table}.slug, {table}.author_id, {table}.body, postable.created_at, ' \
            'postable.updated_at FROM {schema}{table} INNER JOIN {schema}postable ON {table}.id = postable.id WHERE ' \
            '{table}.slug = $1'

        return await self.fetch(q, args=(slug,), single=True, flatten=True)

    async def create(self, title: str, slug: str, author: int, body: str) -> str:
        """
        Create a blog entry.

        :param title:
        :param slug:
        :param author:
        :param body:
        :return:
        """
        i = 'WITH entry_id as (INSERT INTO {schema}postable (created_at, updated_at) VALUES ($5, $6) RETURNING id) ' \
            'INSERT INTO {schema}{table} (id, title, slug, author_id, body) VALUES (' \
            '(SELECT id FROM entry_id LIMIT 1), $1, $2, $3, $4) RETURNING id, title, slug, author_id, body'

        return await self.fetch(i, args=(title, slug, author, body, *self.timestamps()), single=True, flatten=True)


class Comment(Model):
    pass
