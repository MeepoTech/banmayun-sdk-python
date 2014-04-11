import json
import io
import socket
import sys
import urllib3


SDK_VERSION = "1.0.0-prealpha"


class RESTResponse(io.IOBase):
    def __init__(self, resp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urllib3_response = resp
        self.status = resp.status
        self.version = resp.version
        self.reason = resp.reason
        self.strict = resp.strict
        self.is_closed = False

    def __del__(self):
        self.close()

    def __exit__(self, typ, value, traceback):
        self.close()

    def read(self, amt=None):
        if self.is_closed:
            raise ValueError('Response already closed')
        return self.urllib3_response.read(amt)

    BLOCK_SIZE = 4 * 1024 * 1024

    def close(self):
        if self.is_closed:
            return

        while self.read(RESTResponse.BLOCK_SIZE):
            pass

        self.is_closed = True
        self.urllib3_response.release_conn()

    @property
    def closed(self):
        return self.is_closed

    def getheaders(self):
        return self.urllib3_response.getheaders()

    def getheader(self, name, default=None):
        return self.urllib3_response.getheader(name, default)

    def fileno(self):
        return self.urllib3_response.fileno()

    def flush(self):
        return self.urllib3_response.flush()


def create_connection(address):
    host, port = address
    err = None
    for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket.socket(af, socktype, proto)
            sock.connect(sa)
            return sock

        except socket.error as e:
            err = e
            if sock is not None:
                sock.close()

    if err is not None:
        raise err
    else:
        raise socket.error("getaddrinfo returns an empty list")


def json_loadb(data):
    if sys.version_info >= (3,):
        data = data.decode('utf8')
    return json.loads(data)


class RESTClientObject(object):
    def __init__(self, max_reusable_connections=8, mock_urlopen=None):
        self.mock_urlopen = mock_urlopen
        self.pool_manager = urllib3.PoolManager(
            num_pools=4,
            maxsize=max_reusable_connections,
            block=False,
            timeout=10.0
        )

    def request(self, method, url, headers=None, body=None, raw_response=False):
        headers = headers or {}
        headers['User-Agent'] = 'OfficialBanmayunPythonSDK/' + SDK_VERSION

        if hasattr(body, 'getvalue'):
            body = str(body.getvalue())
            headers["Content-Length"] = len(body)

        for key, value in headers.items():
            if isinstance(value, str) and '\n' in value:
                raise ValueError("headers should not contain newlines (%s: %s)" %
                                 (key, value))

        try:
            urlopen = self.mock_urlopen if self.mock_urlopen else self.pool_manager.urlopen
            r = urlopen(
                method=method,
                url=url,
                body=body,
                headers=headers,
                preload_content=False
            )
            r = RESTResponse(r)
        except socket.error as e:
            raise RESTSocketError(url, e)
        except urllib3.exceptions.SSLError as e:
            raise RESTSocketError(url, "SSL certificate error: %s" % e)

        if r.status != 200:
            raise ErrorResponse(r, r.read())

        return self.process_response(r, raw_response)

    def process_response(self, r, raw_response):
        if raw_response:
            return r
        else:
            s = r.read()
            try:
                resp = json_loadb(s)
            except ValueError:
                raise ErrorResponse(r, s)
            r.close()

        return resp

    def GET(self, url, headers=None, raw_response=False):
        assert type(raw_response) == bool
        return self.request("GET", url, headers=headers, raw_response=raw_response)

    def POST(self, url, headers=None, body=None, raw_response=False):
        assert type(raw_response) == bool
        return self.request("POST", url, headers=headers, body=body, raw_response=raw_response)

    def PUT(self, url, headers=None, body=None, raw_response=False):
        assert type(raw_response) == bool
        return self.request("PUT", url, headers=headers, body=body, raw_response=raw_response)

    def DELETE(self, url, headers=None, raw_response=False):
        assert type(raw_response) == bool
        return self.request("DELETE", url, headers=headers, raw_response=raw_response)


class RESTClient(object):
    IMPL = RESTClientObject()

    @classmethod
    def request(cls, *n, **kw):
        return cls.IMPL.request(*n, **kw)

    @classmethod
    def GET(cls, *n, **kw):
        return cls.IMPL.GET(*n, **kw)

    @classmethod
    def POST(cls, *n, **kw):
        return cls.IMPL.POST(*n, **kw)

    @classmethod
    def PUT(cls, *n, **kw):
        return cls.IMPL.PUT(*n, **kw)

    @classmethod
    def DELETE(cls, *n, **kw):
        return cls.IMPL.DELETE(*n, **kw)


class RESTSocketError(socket.error):
    def __init__(self, host, e):
        msg = "Error connecting to \"%s\": %s" % (host, str(e))
        socket.error.__init__(self, msg)


class ErrorResponse(Exception):
    def __init__(self, http_resp, body):
        self.status = http_resp.status
        self.reason = http_resp.reason
        self.body = body
        self.headers = http_resp.getheaders()
        http_resp.close()

        try:
            self.body = json_loadb(self.body)
            self.code = self.body.get('code')
            self.message = self.body.get('message')
        except ValueError:
            self.code = None
            self.message = None

    def __str__(self):
        if self.code is not None and self.message:
            msg = "[%r] %r" % (self.code, self.message)
        elif not self.body:
            msg = repr(self.reason)
        else:
            msg = "Error parsing response body or headers: " + \
                  "Body - %.100r Headers - %r" % (self.body, self.headers)

        return "[%d] %s" % (self.status, msg)
