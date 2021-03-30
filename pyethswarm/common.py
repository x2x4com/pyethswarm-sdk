#!/usr/bin/env python3
# encoding: utf-8
import requests
from json import loads, JSONDecodeError, dumps
from base64 import b64encode


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

    def __repr__(self):
        return dumps({
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        })

    def __str__(self):
        return self.__repr__()


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

    def call_request(self,
                     method,
                     path,
                     data=None,
                     json: dict = None,
                     headers: Headers = None,
                     timeout: int = 30,
                     stream: bool = False,
                     **kwargs
                     ) -> RetType:
        url = self.url + path
        if headers is None:
            headers = Headers()
        req = None
        kwargs.update({"stream": stream})
        try:
            if json:
                req = requests.request(method, url, json=json, timeout=timeout, headers=headers, **kwargs)
            else:
                req = requests.request(method, url, data=data, timeout=timeout, headers=headers, **kwargs)
        except Exception as e:
            return RetType(500, {}, str(e))
        print("[DEBUG HEADERS] %s" % req.headers)
        ret = RetType(req.status_code, {}, '')
        if req.status_code != requests.codes.ok:

            try:
                ret.data = loads(req.text)
            except JSONDecodeError:
                pass
            if type(ret.data) is dict and 'message' in ret.data:
                ret.msg = ret.data['message']
            else:
                ret.msg = req.text
            return ret

        if stream:
            ret.data = {
                "headers": req.headers,
                "raw": b64encode(req.raw.read()).decode()
            }
            # ret.data = req.raw.read()
            # print(ret.data)
        else:
            ret.data = req.json()
        ret.msg = 'ok'

        return ret

    # def call_request(self, method, path, **kwargs):
    #     ret = self._request(method, path, **kwargs)
    #     if ret.code != RetType.OK:
    #         err = ApiError("DEBUG_API", method, path, ret.code, ret.msg)
    #         if self.is_raise:
    #             raise err
    #         # else:
    #         #    print(err)
    #     return ret
