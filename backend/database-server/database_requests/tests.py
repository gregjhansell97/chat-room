from django.contrib.auth.models import User
from django.test import Client, TestCase
import json
import uuid

from database_requests.models import Account


class RequestsFixture(TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "-" * 70)
        print(f"Running {cls.__name__}")
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        print("")

    def post(self, endpoint: str, request: dict):
        """
        returns json content from response
        Args:
            endpoint(str): the endpoint that the call is trying to reach
            request(dict): the request body of the call
        Returns:
            response(dict): the content of the JSONResponse received
        """
        response = self.client.post(
            endpoint, json.dumps(request), content_type="raw"
        )
        return json.loads(response.content)


class TestClientUsage(RequestsFixture):
    def setUp(self):
        """populates database for tests"""
        self.usernames = ["jj-honey", "rc-helicopter", "hubert-sanchez", "gerg", "ethan", "brain", "amazon", "banana"]
        for un in self.usernames:
            # create user and set password
            u = User.objects.create(username=un)
            u.set_password(un)
            u.save()
            # create account
            Account.objects.create(username=un, user=u, token=f"{uuid.uuid4()}")

    def tearDown(self):
        """clears database for future tests"""
        User.objects.all().delete()
        # should cascade down and delete accounts
        assert len(Account.objects.all()) == 0

    def get_token(self, username):
        return self.post("/database/get_token/", {"username": username, "password": username})["token"]

    def test_token_request(self):
        tokens = set()
        # successful logins
        for un in self.usernames:
            response = self.post("/database/get_token/", {"username": un, "password": un})
            assert response["success"]
            assert response["token"] == Account.objects.get(username=un).token
            tokens.add(response["token"])
        assert len(tokens) == len(self.usernames)  # all unique tokens

    def test_one_message_to_one_person(self):
        author = self.usernames[0]
        token = self.get_token(author)
        message = {
            "app": "messenger",
            "token": token,
            "content": {"title": "YUP!"},
            "to_usernames": self.usernames[1:2]
        }
        response = self.post("/database/add_message/", message)
        assert response["success"]
        # verify users receive message
        for un in self.usernames[0:2]:
            un_messages = Account.objects.get(username=un).messages.all()
            assert len(un_messages) == 1
            assert un_messages[0].json() == {"app": message["app"], "content": message["content"], "author": author}
        # verify other users do not receive message
        for un in self.usernames[2:]:
            un_messages = Account.objects.get(username=un).messages.all()
            assert len(un_messages) == 0

    def test_one_message_to_multiple_people(self):
        author = self.usernames[0]
        token = self.get_token(author)
        message = {
            "app": "messenger",
            "token": token,
            "content": {"title": "YUP!"},
            "to_usernames": self.usernames[1:]
        }
        response = self.post("/database/add_message/", message)
        assert response["success"]
        # verify users receive message
        for un in self.usernames:
            un_messages = Account.objects.get(username=un).messages.all()
            assert len(un_messages) == 1
            assert un_messages[0].json() == {"app": message["app"], "content": message["content"], "author": author}

    def test_one_message_to_no_one(self):
        author = self.usernames[0]
        token = self.get_token(author)
        message = {
            "app": "messenger",
            "token": token,
            "content": {"title": "YUP!"},
            "to_usernames": []
        }
        response = self.post("/database/add_message/", message)
        assert response["success"]
        # verify users receive message
        for un in self.usernames[0:1]:
            un_messages = Account.objects.get(username=un).messages.all()
            assert len(un_messages) == 1
            assert un_messages[0].json() == {"app": message["app"], "content": message["content"], "author": author}
        # verify other users do not receive message
        for un in self.usernames[1:]:
            un_messages = Account.objects.get(username=un).messages.all()
            assert len(un_messages) == 0

    def test_many_messages_to_one(self):
        author = self.usernames[0]
        token = self.get_token(author)
        messages = [{
            "app": "messenger",
            "token": token,
            "content": {"title": f"YUP!-{i}"},
            "to_usernames": self.usernames[1:2]
        } for i in range(3)]
        responses = [self.post("/database/add_message/", m) for m in messages]
        assert all([r["success"] for r in responses])
        # verify users receive messages - in order
        for un in self.usernames[0:2]:
            un_messages = Account.objects.get(username=un).messages.all().order_by("timestamp")
            assert len(un_messages) == len(messages)
            for un_m, m in zip(un_messages, messages):
                assert un_m.json() == {"app": m["app"], "content": m["content"], "author": author}
        # verify other users do not receive message
        for un in self.usernames[2:]:
            un_messages = Account.objects.get(username=un).messages.all()
            assert len(un_messages) == 0
