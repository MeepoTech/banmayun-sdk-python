from __future__ import absolute_import

import urllib.parse

from . import rest


class BaseSession(object):
    API_VERSION = 1

    def __init__(self, api_host="api.banmayun.com", locale=None, time_zone=None, rest_client=rest.RESTClient):
        self.api_host = api_host
        self.locale = locale
        self.time_zone = time_zone
        self.rest_client = rest_client
        self.link = None

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
        url = self.build_url('/auth/sign_in')
        params = {'username': username,
                  'password': password,
                  'link_name': link_name,
                  'link_device': link_device}
        headers, params = self.build_access_headers(url, params=params)
        url = self.build_url('/auth/sign_in', params=params)

        self.link = self.rest_client.POST(url, headers=headers)
        return self.link

    def build_access_headers(self, resource_url, params=None):
        if params is None:
            params = {}
        else:
            params = params.copy()

        if self.link:
            params['token'] = self.link["token"]

        return {}, params
