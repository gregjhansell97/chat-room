from django.contrib.auth.models import User
from django.test import Client, TestCase
import json
from typing import List
import uuid

from database_requests.models import Account


class RequestsFixture(TestCase):
    @classmethod
    def setUpClass(class_):
        print("\n" + "-" * 70)
        print(f"Running {class_.__name__}")
        class_.client = Client()

    @classmethod
    def tearDownClass(class_):
        print("")

    def post(self, endpoint: str, request: dict):
        """
        returns json content from reponse
        Args:
            endpoint(str): the endpoint that the call is trying to reach
            request(dict): the request body of the call
        Returns:
            reponse(dict): the content of the JSONResponse received
        """
        response = self.__class__.client.post(
            endpoint, json.dumps(request), content_type="raw"
        )
        return json.loads(response.content)


class TestClientUsage(RequestsFixture):
    def setUp(self):
        """populates database for tests"""
        usernames = ["jj-honey", "rc-helicopter", "hubert-sanchez"]
        users: List[User] = [
            User.objects.get_or_create(username=un)[0] for un in usernames
        ]
        for u in users:
            u.set_password(u.username)
            u.save()
        accounts: List[Account] = [Account.objects.create(user=u) for u in users]
        # save accounts
        for a in accounts:
            a.token = f"{uuid.uuid4()}"
            a.save()
        # field variables
        self.usernames, self.users, self.accounts = usernames, users, accounts

    def tearDown(self):
        """clears database for future tests"""
        User.objects.all().delete()
        # should cascade down and delete accounts
        assert len(Account.objects.all()) == 0

    def test_token_request(self):
        tokens = set()
        for un in self.usernames:
            response = self.post("/database/get_token/", {"username": un, "password": un})
            assert response["success"]
            tokens.add(response["token"])
        assert len(tokens) == len(self.usernames)  # all unique tokens
