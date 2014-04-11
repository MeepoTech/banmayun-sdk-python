from __future__ import absolute_import

import json
import urllib.parse

from . import rest


class BaseSession(object):
    API_VERSION = 1

    def __init__(self, locale=None, time_zone=None, rest_client=rest.RESTClient):
        self.api_host = "api.banmayun.com"
        self.token = None
        self.locale = locale
        self.time_zone = time_zone
        self.rest_client = rest_client

    def is_linked(self):
        return bool(self.token)

    def unlink(self):
        # TODO: logout
        self.token = None

    def build_path(self, target, params=None):
        target_path = urllib.parse.quote(target)

        params = params or {}
        params = params.copy()

        if self.locale:
            params['locale'] = self.locale
        if self.time_zone:
            params['time_zone'] = self.time_zone

        if params:
            return "/%s%s?%s" % (self.API_VERSION, target_path, urllib.parse.urlencode(params))
        else:
            return "/%s%s" % (self.API_VERSION, target_path)

    def build_url(self, target, params=None):
        return "http://%s%s" % (self.api_host, self.build_path(target, params))


class BanmayunSession(BaseSession):
    def set_token(self, token):
        self.token = token

    def obtain_token(self, username, password, link_name, link_device):
        url = self.build_url(self.api_host, '/auth/sign_in')
        params = {'username': username,
                  'password': password,
                  'link_name': link_name,
                  'link_device': link_device}
        headers, params = self.build_access_headers(url, params=params)

        response = self.rest_client.POST(url, headers=headers, params=params, raw_response=True)
        self.token = self._parse_token(response.read())
        return self.token

    def build_access_headers(self, resource_url, params=None):
        if params is None:
            params = {}
        else:
            params = params.copy()

        if self.token:
            params.update({'token', self.token})

        return {}, params

    @classmethod
    def _parse_token(cls, s):
        if not s:
            raise ValueError("Invalid parameter string.")

        params = json.loads(s)
        if not params:
            raise ValueError(u"Invalid parameter string: %r" % s)

        token = params.get("token", None)
        if token is None:
            raise ValueError("'token' not found in response")
        else:
            return token
