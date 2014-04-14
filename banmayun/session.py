from __future__ import absolute_import

import json
import urllib.parse

from . import rest


class BaseSession(object):
    API_VERSION = 1

    def __init__(self, locale=None, time_zone=None, rest_client=rest.RESTClient):
        self.api_host = "api.banmayun.com"
        self.link = None
        self.locale = locale
        self.time_zone = time_zone
        self.rest_client = rest_client

    def set_link(self, link):
        self.link = link

    def get_link(self):
        return self.link

    def is_linked(self):
        return bool(self.link)

    def unlink(self):
        # TODO: logout
        self.link = None

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
    def obtain_link(self, username, password, link_name, link_device):
        url = self.build_url(self.api_host, '/auth/sign_in')
        params = {'username': username,
                  'password': password,
                  'link_name': link_name,
                  'link_device': link_device}
        headers, params = self.build_access_headers(url, params=params)

        response = self.rest_client.POST(url, headers=headers, params=params, raw_response=True)
        self.link = json.loads(response.read())
        return self.link

    def build_access_headers(self, resource_url, params=None):
        if params is None:
            params = {}
        else:
            params = params.copy()

        if self.link:
            params.update({'token', self.link["token"]})

        return {}, params
