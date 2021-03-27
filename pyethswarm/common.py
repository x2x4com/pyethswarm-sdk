#!/usr/bin/env python3
# encoding: utf-8
import requests
from json import loads, JSONDecodeError


class ApiError(Exception):
    def __init__(self, target, method, url, code, msg):
        self.target = target
        self.method = method
        self.url = url
        self.code = code
        self.msg = msg
        err = "[%s]-[%s]-[%s] %s: %s" % (target, method, url, code, msg)
        super().__init__(err)


class RetType(object):
    OK = requests.codes.ok

    def __init__(self, code: int, data: dict, msg: str):
        self.code = code
        self.data = data
        self.msg = msg


class ContentType(object):
    JSON = 'application/json'
    FORM = 'application/x-www-form-urlencoded'
    XTAR = 'application/x-tar'
    MULTIPART = 'multipart/form-data'
    OCTETSTEAM = 'application/octet-stream'


class Headers(dict):
    def __init__(self, t: dict = {}):
        super().__init__()
        self.update({
            "content-type": ContentType.FORM,
            **t
        })


class ClientBase(object):
    is_raise = True

    def __init__(self, url, version):
        self.url = url
        self.__version = version

    @property
    def version(self):
        return self.__version

    def _request(self,
                 method,
                 path,
                 data: dict = None,
                 json: dict = None,
                 headers: Headers = None,
                 timeout: int = 30,
                 **kwargs
                 ) -> RetType:
        url = self.url + path
        if headers is None:
            headers = Headers()
        req = None
        try:
            if json:
                req = requests.request(method, url, json=json, timeout=timeout, headers=headers, **kwargs)
            else:
                req = requests.request(method, url, data=data, timeout=timeout, headers=headers, **kwargs)
        except Exception as e:
            return RetType(500, {}, str(e))
        ret = RetType(req.status_code, {}, '')
        if req.status_code != requests.codes.ok:
            ret.msg = req.text
            try:
                ret.data = loads(ret.msg)
            except JSONDecodeError:
                pass
            return ret

        ret.data = req.json()
        ret.msg = 'ok'

        return ret

    def call_request(self, method, path, **kwargs):
        ret = self._request(method, path, **kwargs)
        if ret.code != RetType.OK:
            err = ApiError("DEBUG_API", method, path, ret.code, ret.msg)
            if self.is_raise:
                raise err
            else:
                print(err)
        return ret.data
