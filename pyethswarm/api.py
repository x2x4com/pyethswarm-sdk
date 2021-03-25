#!/usr/bin/env python3
# encoding: utf-8

from .common import ClientBase, RetType, ApiError, Headers


class Client(ClientBase):
    __version = "0.5.2"

    def __init__(self, url: str = 'http://localhost:1633', is_raise=True):
        super().__init__(url, self.__version)
        self.is_raise = is_raise

    def post_bytes(self, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool):
        method = "POST"
        path = "/bytes"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin,
            "swarm-encrypt": swarm_encrypt
        })
        return self.call_request(method, path, headers=headers)

    def get_bytes(self, reference: str):
        method = "GET"
        path = "/bytes/%s" % reference
        return self.call_request(method, path)

    def get_chunks(self, reference: str):
        method = "GET"
        path = "/chunks/%s" % reference
        return self.call_request(method, path)

    def post_chunks(self, string_bin: bytes, swarm_tag: int, swarm_pin: bool):
        method = "POST"
        path = "/chunks"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin
        })
        headers['content_type'] = "application/octet-stream"
        return self.call_request(method, path, headers=headers, data=string_bin)

    def get_files(self, reference: str):
        method = "GET"
        path = "/files/%s" % reference
        return self.call_request(method, path)

    def post_files(self, file_name: str, file_bin: bytes, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool):
        method = "POST"
        path = "/files?name=" % file_name
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin,
            "swarm-encrypt": swarm_encrypt
        })
        headers['content-type'] = "multipart/form-data"
        return self.call_request(method, path, headers=headers, data=file_bin)
