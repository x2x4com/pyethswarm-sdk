#!/usr/bin/env python3
# encoding: utf-8
import requests


class ApiError(Exception):
    def __init__(self, target, method, url, code, msg):
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
    FORM = 'application/x-www-form-urlencoded '


class Headers(dict):
    def __init__(self, t: dict = {}):
        super().__init__()
        self.update({
            "content-type": ContentType.FORM,
            **t
        })


class ClientBase(object):
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
                 headers: Headers = Headers,
                 timeout: int = 30
                 ) -> RetType:
        url = self.url + path

        req = None
        try:
            if data:
                req = requests.request(method, url, data=data, timeout=timeout, headers=headers)
            if json:
                req = requests.request(method, url, json=json, timeout=timeout, headers=headers)
        except Exception as e:
            return RetType(500, {}, str(e))

        ret = RetType(req.status_code, {}, '')
        if req.status_code != requests.codes.ok:
            ret.msg = req.text
            return ret

        ret.data = req.json()
        ret.msg = 'ok'
        return ret
