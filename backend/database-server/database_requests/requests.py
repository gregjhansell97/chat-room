from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import json
import uuid
import traceback

from database_requests.models import Account, Message


def json_wrapper(func):
    """wraps a function that receives json data, and dumps that data to func

    Args:
        func(function): takes in named arguments

    Return:
        (function): wrapped function
    """

    def wrapper(request):
        data = json.loads(request.body.decode("utf-8"))
        try:
            response = func(**data)
            if not response:
                response = {}
            response = {"success": True, **response}
            return JsonResponse(response)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"success": False, "error": f"{e} - look at server logs for more details"})
    wrapper.json_wrapper = True
    return wrapper


def token_wrapper(func):
    """wraps a function and uses the token keyword passed into it to remap that to a username and password

    Args:
        func(function): takes in named arguments

    Return:
        (function): wrapped function
    """
    def wrapper(token=None, **kwargs):
        account = Account.objects.get(token=token)
        return func(**{**kwargs, "account": account})
    return wrapper


@json_wrapper
def get_token(*, username: str, password: str):
    """ Takes in a username and password and returns a dictionary of data - specifically the token

        Args:
            username (str): username trying to get token
            password (str): password for that user
        Returns:
            (dict): a dictionary of the fields available and success of query
            {
                token (int): token so username and password are not used every time
            }
    """
    try:
        login_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("either username or password is invalid")  # not exposing which one

    if check_password(password, login_user.password):
        # TODO: change login_token to something other than username
        login_token = f"{uuid.uuid4()}"
        account, _ = Account.objects.get_or_create(user=login_user)
        account.token = login_token
        account.save()
        return {"token": login_token}
    raise ValueError("either username or password is invalid")


@json_wrapper
@token_wrapper
def add_message(*, app: str, account: Account, content: dict, to_usernames: list):
    """TODO: explain"""
    m = Message.objects.create(app=app, author=account, content=content)
    to_accounts = [Account.objects.get(username=u) for u in to_usernames] + [account]
    for a in to_accounts:
        a.messages.add(m)
        a.save()
    return {}


@json_wrapper
def set_checkpoint(*, app: str, checkpoint: dict):
    # grab checkpoint
    pass


@json_wrapper
def get_checkpoint(*, app: str):
    # grab checkpoint and return it!
    pass
