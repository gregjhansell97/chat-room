# -*- coding: utf-8 -*-
"""
Add admin details for the backend app; models used in admin are registered in
this file
"""
from django.contrib import admin

from database_requests.models import Account

# makes accounts editable on the admin server
admin.site.register(Account)
