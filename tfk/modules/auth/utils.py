from typing import Union
from functools import wraps
from ryoken.regexes import Regexinator

REGEXINATOR = Regexinator()


async def validate_password(length: int, value: str, r_value: str = None, weak: bool = True, repeat: bool = True,
                            regexinator: Regexinator = REGEXINATOR) -> Union[dict, bool]:
    result = dict()

    if not value:
        result['p'] = 'You cannot leave the password field empty'
    elif repeat and not r_value:
        result['r'] = 'You cannot leave the repeat password field empty'
    elif length < 6 or length > 128:
        result['p'] = 'Password must be longer than 6 characters but less than or equal to 128'
    elif repeat and value != r_value:
        result['r'] = "Password and repeated password fields don't match"
    elif not weak and not (await regexinator.validate(value, strategy='PASSWORD')):
        result['p'] = 'Password too weak, it must contain at least 3 numbers and 3 letters'

    return result or True


async def validate_username(length: int, value: str, regexinator: Regexinator = REGEXINATOR) -> Union[dict, bool]:
    result = dict()

    if not value:
        result['u'] = 'You cannot leave the username field empty'
    elif length < 4 or length > 16:
        result['u'] = 'Username must be longer than 4 characters but less than or equal to 16'
    elif not (await regexinator.validate(value, strategy='USERNAME')):
        result['u'] = 'Username must only contain a-z, A-Z, and 0-9'

    return result or True


async def validate_email(length: int, value: str, regexinator: Regexinator = REGEXINATOR) -> Union[dict, bool]:
    result = dict()

    if not value:
        result['e'] = 'You cannot leave the email field empty'
    elif length < 16 or length > 64:
        result['e'] = 'Email must be longer than 16 characters but less than or equal to 64'
    elif not (await regexinator.validate(value, strategy='EMAIL')):
        result['e'] = 'Email not valid'

    return result or True


def authenticated(is_authenticated: bool):
    def request_handler(coro):
        @wraps(coro)
        async def handle(*args, **kwargs):
            # Convert arguments tuple to a list
            args = list(args)

            # Get the request object and remove it from the list
            request = args[1]

            # Model
            user_model, auth_model = request.app.models.auth_user, request.app.models.auth_authenticable

            # Token string
            token = None

            if 'authorization' in request.headers:
                token = request.headers['authorization']

                if not isinstance(token, str):
                    raise Exception

            if not is_authenticated:
                if not token:
                    return await coro(*args, **kwargs)
                else:
                    raise Exception

            if not token:
                raise Exception

            _user = await auth_model.get_user(token)

            if not _user:
                raise Exception

            user = await user_model.get_single(_user['id'])

            del _user

            args.insert(2, user)

            return await coro(*args, **kwargs)
        return handle
    return request_handler
