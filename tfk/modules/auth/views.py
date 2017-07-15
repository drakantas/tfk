from datetime import datetime

from bcrypt import checkpw, gensalt, hashpw
from sanic.response import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from ryoken.tokenizer import Tokenizer
from ryoken.collections import StrLengthDict

from ...utils import check_payload
from .utils import authenticated, validate_email, validate_username, validate_password

TOKENIZER = Tokenizer()


class RegisterUser(HTTPMethodView):
    @authenticated(False)
    async def post(self, request: Request):
        payload = check_payload(request, self)

        validated_data = await self._validate(payload)

        if not validated_data['errors']:
            user = await self._create(validated_data, request)

            del validated_data

            return json(user)

        return json(validated_data, status=422)

    async def _create(self, data: dict, request: Request) -> dict:
        # Model instances
        user_model, authenticable_model = request.app.models.auth_user, request.app.models.auth_authenticable

        hashed_pw = hashpw(data['p'].encode('utf-8'), gensalt()).decode('utf-8')

        # Create user in the database
        user = await user_model.create(data['u'], data['e'], hashed_pw, data['a'].encode('utf-8') or None)

        packed_token = await self._generate_token((user['id'], round(datetime.utcnow().timestamp() * 10 ** 6), 1))

        # Token of user
        token = await authenticable_model.create(user['id'], packed_token[0], packed_token[1])

        # Delete from memory because it's no longer needed
        del user_model, authenticable_model, data, hashed_pw, packed_token

        return {**user,
                **token}

    @staticmethod
    async def _validate(data: dict) -> dict:
        # Dictionary which values are tuples of the order (key_length, actual_value)
        data = StrLengthDict(data)

        # Result data dict
        result_data = {key: value[1] for key, value in data.items()}

        # This will be parsed into a JSON object with all of the validation messages
        result_data['errors'] = {}

        # Username validations
        username = await validate_username(data['u'][0], data['u'][1])

        # Email validations
        email = await validate_email(data['e'][0], data['e'][1])

        # Password validations
        password = await validate_password(data['p'][0], data['p'][1], data['r'][1], weak=False)

        # If we get errors then add them to the resultant data
        if isinstance(username, dict):
            result_data['errors'].update(username)

        if isinstance(email, dict):
            result_data['errors'].update(email)

        if isinstance(password, dict):
            result_data['errors'].update(password)

        # No longer needed
        del data, email, username, password

        return result_data

    @staticmethod
    async def _generate_token(data: tuple) -> tuple:
        return tuple(map(lambda e: e.decode('utf-8'), (await TOKENIZER.generate(data))))

    @staticmethod
    def _payload_fields():
        return {
            'u': str,
            'e': str,
            'p': str,
            'r': str,
            'a': str
        }


class Login(HTTPMethodView):
    @authenticated(False)
    async def post(self, request: Request):
        payload = check_payload(request, self)

        validated_data = await self._validate(payload, request)

        if not validated_data['errors']:
            return json(await self._auth(validated_data, request))

        return json(validated_data, status=401)

    @staticmethod
    async def _auth(data: dict, request: Request) -> dict:
        authenticable_model = request.app.models.auth_authenticable

        return await authenticable_model.get_token(data['_id'])

    @staticmethod
    async def _validate(data: dict, request: Request) -> dict:
        user_model = request.app.models.auth_user

        data = StrLengthDict(data)

        result_data = {key: value[1] for key, value in data.items()}

        result_data['errors'] = {}

        email = await validate_email(data['e'][0], data['e'][1])

        password = await validate_password(data['p'][0], data['p'][1], repeat=False, weak=True)

        _user = None

        if isinstance(email, dict):
            result_data['errors'].update(email)
        else:
            _user = await user_model.get_single_by_email(data['e'][1])

            if not _user:
                result_data['errors']['e'] = 'No associated user found for this email'

        if isinstance(password, dict):
            result_data['errors'].update(password)
        else:
            if _user:
                if not checkpw(data['p'][1].encode('utf-8'), _user['password'].encode('utf-8')):
                    result_data['errors']['p'] = 'Incorrect password. Try again'
                else:
                    result_data['_id'] = _user['id']

        # No longer needed
        del data, email, password, _user

        return result_data

    @staticmethod
    def _payload_fields():
        return {
            'e': str,
            'p': str
        }
