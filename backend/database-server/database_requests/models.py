from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import (
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
    TextField,
)
import json


class JSONField(TextField):
    """
    JSONField is a generic textfield that neatly serializes/deserializes JSON objects seamlessly. Information was
    grabbed from the url below and modified:
    https://stackoverflow.com/questions/9686409/how-to-store-a-dictionary-in-a-django-database-models-field

    Example:
    ::
        class Page(models.Model):
            data = JSONField(blank=True, null=True)
        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def __init__(*args, **kwargs):
        TextField.__init__(*args, **kwargs)

    def to_python(self, value):
        """
        overrides TextField's to_python method
        """
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value):
        """
        overrides TextField's from_db_value method
        """
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        """
        overrides TextField's get_db_prep_save method
        """
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value


class Message(Model):
    """model for each message in the system"""

    app: TextField = TextField(default="")
    """app the message is intended for"""

    author: OneToOneField = OneToOneField("Account", on_delete=models.CASCADE)
    """creator of message"""

    content: JSONField = JSONField(default={})
    """data the message contains"""

    timestamp: DateTimeField = DateTimeField(auto_now_add=True)
    """when the message was created"""


class Snapshot(Model):
    """model for each checkpoint of the system"""

    app: TextField = TextField()
    """app the content is intended for"""

    content: JSONField
    """information for the checkpoint"""

    timestamp: DateTimeField = DateTimeField(auto_now_add=True)
    """when the checkpoint was created"""

    account = ForeignKey("Account", on_delete=models.CASCADE)


class Account(Model):
    """this table is a proxy table to an already existing user table; it allows
    non security-related fields to be tied to a user
    """

    user: OneToOneField = OneToOneField(User, on_delete=models.CASCADE)
    """connects a TokenUser to a User"""

    token: TextField = TextField(default="", blank=True)
    """token used to access account without carrying around around a password"""

    messages: ManyToManyField = ManyToManyField(Message)
    """messages tied to the account"""
