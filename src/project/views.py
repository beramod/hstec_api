from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.shortcuts import render_to_response
import datetime


import logging
_LOG = logging.getLogger(__name__)


class TemplateView(View):
    def set_cookie(self, response, key, value, days_expire = 7):
        if days_expire is None:
            max_age = 365 * 24 * 60 * 60  #one year
        else:
            max_age = days_expire * 24 * 60 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, expires=expires)
        #response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

    def get(self, request):

        response = render_to_response('index.html')

        return response