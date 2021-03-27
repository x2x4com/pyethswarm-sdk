#!/usr/bin/env python3
# encoding: utf-8
from urllib.parse import urlencode
from .common import ClientBase, RetType, ApiError, Headers, ContentType
from .address import ChunkAddress, ContentAddress, PeerAddress


class Client(ClientBase):
    __version = "0.5.2"

    def __init__(self, url: str = 'http://localhost:1633', is_raise=True):
        super().__init__(url, self.__version)
        self.is_raise = is_raise

    def post_bytes(self, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool):
        method = "POST"
        path = "/bytes"
        headers = Headers({
            # 预先生成的tag
            "swarm-tag": swarm_tag,
            # 是否持久化
            "swarm-pin": swarm_pin,
            "swarm-encrypt": swarm_encrypt
        })
        return self.call_request(method, path, headers=headers)

    def get_bytes(self, reference: str):
        method = "GET"
        path = "/bytes/%s" % ContentAddress(reference)
        return self.call_request(method, path)

    def get_chunks(self, reference: str):
        method = "GET"
        path = "/chunks/%s" % ChunkAddress(reference)
        return self.call_request(method, path)

    def post_chunks(self, string_bin: bytes, swarm_tag: int, swarm_pin: bool):
        method = "POST"
        path = "/chunks"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin
        })
        headers['content_type'] = ContentType.OCTETSTEAM
        return self.call_request(method, path, headers=headers, data=string_bin)

    def get_files(self, reference: str):
        method = "GET"
        path = "/files/%s" % ChunkAddress(reference)
        return self.call_request(method, path)

    def upload_files(self, file_name: str, file_bin: bytes, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool):
        method = "POST"
        path = "/files?%s" % urlencode({"name": file_name})
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin,
            "swarm-encrypt": swarm_encrypt
        })
        # headers['content-type'] = "multipart/form-data"
        headers['content-type'] = ContentType.OCTETSTEAM
        return self.call_request(method, path, headers=headers, data=file_bin)

    def upload_collection(self,
                          collection_bin: bytes,
                          swarm_tag: int,
                          swarm_pin: bool,
                          swarm_encrypt: bool,
                          swarm_index_document: str,
                          swarm_error_document: str
                          ):
        method = "POST"
        path = "/dirs"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin,
            "swarm-encrypt": swarm_encrypt,
            "swarm-index-document": swarm_index_document,
            "swarm-error-document": swarm_error_document
        })
        headers['content-type'] = ContentType.XTAR
        return self.call_request(method, path, headers=headers, data=collection_bin)

    def get_collection_index(self, reference: str, targets: str):
        """
        https://docs.ethswarm.org/docs/advanced/persistence#global-pinning

        :param reference:
        :param targets: global-pinning， 需要在节点打开global-pinning-enable标签，
        :return:
        """
        method = "GET"
        path = "/bzz/%s?%s" % (ChunkAddress(reference), urlencode({"targets": targets}))
        return self.call_request(method, path)

    def get_connection_file(self, reference: str, file_path: str, targets: str):
        method = "GET"
        path = "/bzz/%s/%s?%s" % (reference, file_path, urlencode({"targets": targets}))
        return self.call_request(method, path)

    def get_tags(self, uid: str = None, offset: int = 0, limit: int = 0):
        method = "GET"
        if uid is not None:
            path = "/tags/%s" % uid
        else:
            path = "/tags?%s" % urlencode({"offset": offset, "limit": limit})
        return self.call_request(method, path)

    def create_tag(self, address: str):
        method = "POST"
        path = "/tags"
        data = {
            "address": PeerAddress(address)
        }
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        return self.call_request(method, path, headers=headers, json=data)

    def delete_tag(self, uid: int):
        method = "DELETE"
        path = "/tags/%s" % uid
        return self.call_request(method, path)

    def update_tag(self, uid: int, address: str):
        method = "PATCH"
        path = "/tags/%s" % uid
        data = {
            "address": PeerAddress(address)
        }
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        return self.call_request(method, path, headers=headers, json=data)





