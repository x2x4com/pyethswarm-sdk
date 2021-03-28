#!/usr/bin/env python3
# encoding: utf-8
from urllib.parse import urlencode
from .common import ClientBase, Headers, ContentType
from .address import *
from time import time


class Client(ClientBase):
    __version = "0.5.2"

    def __init__(self, url: str = 'http://localhost:1633', is_raise=True):
        super().__init__(url, self.__version)
        self.is_raise = is_raise

    def create_bytes(self, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool):
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

    def create_chunks(self, string_bin: bytes, swarm_tag: int, swarm_pin: bool):
        method = "POST"
        path = "/chunks"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin
        })
        headers['content-type'] = ContentType.OCTETSTEAM
        return self.call_request(method, path, headers=headers, data=string_bin)

    def get_files(self, reference: str):
        method = "GET"
        path = "/files/%s" % ContentAddress(reference)
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
        path = "/bzz/%s?%s" % (CollectionAddress(reference), urlencode({"targets": targets}))
        return self.call_request(method, path)

    def get_collection_file(self, reference: str, file_path: str, targets: str):
        method = "GET"
        path = "/bzz/%s/%s?%s" % (CollectionAddress(reference), file_path, urlencode({"targets": targets}))
        return self.call_request(method, path)

    def get_tags(self, uid: str = None, offset: int = 0, limit: int = 0):
        method = "GET"
        if uid is not None:
            path = "/tags/%s" % uid
        else:
            path = "/tags?%s" % urlencode({"offset": offset, "limit": limit})
        return self.call_request(method, path)

    def create_tag(self, peer_address: str):
        method = "POST"
        path = "/tags"
        data = {
            "address": PeerAddress(peer_address)
        }
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        return self.call_request(method, path, headers=headers, json=data)

    def delete_tag(self, uid: int):
        method = "DELETE"
        path = "/tags/%s" % uid
        return self.call_request(method, path)

    def update_tag(self, uid: int, peer_address: str):
        method = "PATCH"
        path = "/tags/%s" % uid
        data = {
            "address": PeerAddress(peer_address)
        }
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        return self.call_request(method, path, headers=headers, json=data)

    def create_pin_chunk(self, chunk_address: str):
        method = "POST"
        path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path)

    def get_pin_chunk(self, chunk_address: str = None, offset: int = 0, limit: int = 0):
        method = "GET"
        if chunk_address is None:
            path = "/pin/chunks?%s" % urlencode({"offset": offset, "limit": limit})
        else:
            path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path)

    def update_pin_chunk(self, chunk_address: str):
        method = "PUT"
        path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path)

    def delete_pin_chunk(self, chunk_address: str):
        method = "DELETE"
        path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path)

    def create_pin_bytes(self, bytes_address: str):
        method = "POST"
        path = "/pin/bytes/%s" % BytesAddress(bytes_address)
        return self.call_request(method, path)

    def delete_pin_bytes(self, bytes_address: str):
        method = "DELETE"
        path = "/pin/bytes/%s" % BytesAddress(bytes_address)
        return self.call_request(method, path)

    def create_pin_files(self, file_address: str):
        method = "POST"
        path = "/pin/files/%s" % FileAddress(file_address)
        return self.call_request(method, path)

    def delete_pin_files(self, file_address: str):
        method = "POST"
        path = "/pin/files/%s" % FileAddress(file_address)
        return self.call_request(method, path)

    def create_pin_collection(self, collection_address: str):
        method = "POST"
        path = "/pin/bzz/%s" % CollectionAddress(collection_address)
        return self.call_request(method, path)

    def delete_pin_collection(self, collection_address: str):
        method = "POST"
        path = "/pin/bzz/%s" % CollectionAddress(collection_address)
        return self.call_request(method, path)

    def send_pss(self, topic: str, targets: str):
        method = "POST"
        path = "/pss/send/{topic}/{targets}".format(topic=topic, targets=targets)
        return self.call_request(method, path)

    def subscribe_pss(self, topic: str):
        method = "GET"
        path = "/pss/subscribe/{topic}".format(topic=topic)
        return self.call_request(method, path)

    def create_single_owner_chunk(self, owner: str, _id: str, sig: str):
        method = "POST"
        path = "/soc/{owner}/{id}?{query}".format(
            owner=OwnerAddress(owner),
            id=IdAddress(_id),
            query=urlencode({"sig": sig})
        )
        return self.call_request(method, path)

    def create_feed(self, owner: str, topic: str, swarm_pin: bool, _type: str = "sequence"):
        method = "POST"
        if _type not in ["sequence", "epoch"]:
            _type = "sequence"
        path = "/feeds/{owner}/{topic}?{query}".format(
            owner=OwnerAddress(owner),
            topic=IdAddress(topic),
            query=urlencode({"type": _type})
        )
        headers = Headers({
            "swarm-pin": swarm_pin
        })
        return self.call_request(method, path, headers=headers)

    def get_feed(self, owner: str, topic: str, at: int = None, _type: str = "sequence"):
        method = "GET"
        if _type not in ["sequence", "epoch"]:
            _type = "sequence"
        if at is None:
            at = int(time())
        path = "/feeds/{owner}/{topic}?{query}".format(
            owner=OwnerAddress(owner),
            topic=IdAddress(topic),
            query=urlencode({"type": _type, "at": at})
        )
        return self.call_request(method, path)