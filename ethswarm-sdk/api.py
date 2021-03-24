#!/usr/bin/env python3
# encoding: utf-8

from common import ClientBase, RetType, ApiError


class Client(ClientBase):
    __version = "0.5.2"

    def __init__(self, url: str = 'http://localhost:1633'):
        super().__init__(url, self.__version)

    def __call_request(self, method, path, *args, **kwargs):
        ret = self._request(method, path, *args, **kwargs)
        if ret.code != RetType.OK:
            raise ApiError('API', method, path, ret.code, ret.msg)
        return ret.data

