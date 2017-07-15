from ...models import Model


class User(Model):
    TABLE_NAME = 'user'

    async def create(self, username: str, email: str, password: str, avatar: bytearray = None):
        i = 'INSERT INTO {schema}{table} (username, email, password, avatar, created_at, updated_at) VALUES (' \
            '$1, $2, $3, $4, $5, $6) RETURNING id, username, email, avatar'

        return await self.fetch(i, (username, email, password, avatar, *self.timestamps()), single=True,
                                flatten=True)

    async def get_single_by_email(self, email: str):
        q = 'SELECT id, password FROM {schema}{table} WHERE email = $1 LIMIT 1'

        return await self.fetch(q, (email,), single=True, flatten=True)

    async def get_single(self, user_id: int):
        q = 'SELECT id, username, email, avatar FROM {schema}{table} WHERE id = $1 LIMIT 1'

        return await self.fetch(q, (user_id,), single=True, flatten=True)


class Authenticable(Model):
    TABLE_NAME = 'authenticable'

    async def create(self, user_id: int, token: str, secret: str):
        i = 'INSERT INTO {schema}{table} (id, token, secret) VALUES ($1, $2, $3) RETURNING token'

        return await self.fetch(i, (user_id, token, secret), single=True, flatten=True)

    async def get_token(self, user_id: int):
        q = 'SELECT token FROM {schema}{table} WHERE id = $1 LIMIT 1'

        return await self.fetch(q, (user_id,), single=True, flatten=True)

    async def get_user(self, token: str):
        q = 'SELECT id FROM {schema}{table} WHERE token = $1 LIMIT 1'

        return await self.fetch(q, (token,), single=True, flatten=True)
