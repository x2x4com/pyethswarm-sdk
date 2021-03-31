#!/usr/bin/env python3
# encoding: utf-8
from urllib.parse import urlencode
from .common import ClientBase, Headers, ContentType
from .address import *
from time import time
import re


class Client(ClientBase):
    __version = "0.5.2"

    def __init__(self, url: str = 'http://localhost:1633', is_raise=True):
        super().__init__(url, self.__version)
        self.is_raise = is_raise

    def create_bytes(self, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool, **kwargs):
        method = "POST"
        path = "/bytes"
        headers = Headers({
            # 预先生成的tag
            "swarm-tag": swarm_tag,
            # 是否持久化
            "swarm-pin": swarm_pin,
            "swarm-encrypt": swarm_encrypt
        })
        return self.call_request(method, path, headers=headers, **kwargs)

    def get_bytes(self, reference: str, **kwargs):
        method = "GET"
        path = "/bytes/%s" % ContentAddress(reference)
        return self.call_request(method, path, **kwargs)

    def get_chunks(self, reference: str, **kwargs):
        method = "GET"
        path = "/chunks/%s" % ChunkAddress(reference)
        return self.call_request(method, path, **kwargs)

    def create_chunks(self, string_bin: bytes, swarm_tag: int, swarm_pin: bool, **kwargs):
        method = "POST"
        path = "/chunks"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin
        })
        headers['content-type'] = ContentType.OCTETSTEAM
        return self.call_request(method, path, headers=headers, data=string_bin, **kwargs)

    def get_files(self, reference: str, **kwargs):
        """
        Get file via reference(Content Address)

        Args:
            reference: Content Address

        Returns:
            existed: return dict({"name": str, "content_type": str, "msg": str, "data": base64encode(byte) })
            not existed: RetType object

        """
        method = "GET"
        path = "/files/%s" % ContentAddress(reference)
        ret = self.call_request(method, path, stream=True, **kwargs)
        if ret.code != 200:
            return ret
        _ret_data = ret.data
        _reg = re.compile(r'filename="(.*)"').findall(_ret_data['headers']['Content-Disposition'])
        msg = "OK"
        if len(_reg) > 0:
            file_name = _reg[0]
        else:
            file_name = _ret_data['headers']['Content-Disposition']
            msg = "Can not find file name, use Content-Disposition instead"
        return {
            "name": file_name,
            "content_type": _ret_data['headers']['Content-Type'],
            "msg": msg,
            "data": _ret_data['raw']
        }

    def upload_files(self,
                     file_name: str,
                     content_type: str,
                     file_bin: bytes,
                     swarm_tag: int = None,
                     swarm_pin: bool = False,
                     swarm_encrypt: bool = False,
                     **kwargs
                     ):
        """
        Upload file,

        Args:
            file_name: file name
            content_type:  file type
            file_bin:  file byte
            swarm_tag:  tag id
            swarm_pin:  bool default false
            swarm_encrypt: bool default false

        Returns:
            ok: return dict({"name": str, "reference": str})
            error: RetType object

        """
        method = "POST"
        path = "/files?%s" % urlencode({"name": file_name})
        if swarm_tag is not None:
            headers = Headers({
                "swarm-tag": swarm_tag,
                "swarm-pin": swarm_pin.__str__().lower(),
                "swarm-encrypt": swarm_encrypt.__str__().lower()
            })
        else:
            headers = Headers({
                "swarm-pin": swarm_pin.__str__().lower(),
                "swarm-encrypt": swarm_encrypt.__str__().lower()
            })
        # headers['content-type'] = "multipart/form-data"
        headers['content-type'] = content_type
        # print(headers)
        ret = self.call_request(method, path, headers=headers, data=file_bin, **kwargs)
        if ret.code != 200:
            return ret
        return {
            "name": file_name,
            **ret.data
        }

    def upload_collection(self,
                          collection_bin: bytes,
                          swarm_tag: int = None,
                          swarm_pin: bool = False,
                          swarm_encrypt: bool = False,
                          swarm_index_document: str = "index.html",
                          swarm_error_document: str = "error.html",
                          **kwargs
                          ):
        method = "POST"
        path = "/dirs"
        if swarm_tag is not None:
            headers = Headers({
                "swarm-tag": swarm_tag,
                "swarm-pin": swarm_pin.__str__().lower(),
                "swarm-encrypt": swarm_encrypt.__str__().lower(),
                "swarm-index-document": swarm_index_document,
                "swarm-error-document": swarm_error_document
            })
        else:
            headers = Headers({
                "swarm-pin": swarm_pin.__str__().lower(),
                "swarm-encrypt": swarm_encrypt.__str__().lower(),
                "swarm-index-document": swarm_index_document,
                "swarm-error-document": swarm_error_document
            })
        headers['content-type'] = ContentType.XTAR
        return self.call_request(method, path, headers=headers, data=collection_bin, **kwargs)

    def get_collection_index(self, reference: str, targets: str, **kwargs):
        """
        https://docs.ethswarm.org/docs/advanced/persistence#global-pinning

        :param reference:
        :param targets: global-pinning， 需要在节点打开global-pinning-enable标签，
        :return:
        """
        method = "GET"
        path = "/bzz/%s?%s" % (CollectionAddress(reference), urlencode({"targets": targets}))
        return self.call_request(method, path, **kwargs)

    def get_collection_file(self, reference: str, file_path: str, targets: str, **kwargs):
        method = "GET"
        path = "/bzz/%s/%s?%s" % (CollectionAddress(reference), file_path, urlencode({"targets": targets}))
        return self.call_request(method, path, **kwargs)

    def get_tags(self, uid: str = None, offset: int = 0, limit: int = 0, **kwargs):
        method = "GET"
        if uid is not None:
            path = "/tags/%s" % uid
        else:
            path = "/tags?%s" % urlencode({"offset": offset, "limit": limit})
        return self.call_request(method, path, **kwargs)

    def create_tag(self, peer_address: str, **kwargs):
        method = "POST"
        path = "/tags"
        data = {
            "address": PeerAddress(peer_address)
        }
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        return self.call_request(method, path, headers=headers, json=data, **kwargs)

    def delete_tag(self, uid: int, **kwargs):
        method = "DELETE"
        path = "/tags/%s" % uid
        return self.call_request(method, path, **kwargs)

    def update_tag(self, uid: int, peer_address: str, **kwargs):
        method = "PATCH"
        path = "/tags/%s" % uid
        data = {
            "address": PeerAddress(peer_address)
        }
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        return self.call_request(method, path, headers=headers, json=data, **kwargs)

    def create_pin_chunk(self, chunk_address: str, **kwargs):
        method = "POST"
        path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path, **kwargs)

    def get_pin_chunk(self, chunk_address: str = None, offset: int = 0, limit: int = 0, **kwargs):
        method = "GET"
        if chunk_address is None:
            path = "/pin/chunks?%s" % urlencode({"offset": offset, "limit": limit})
        else:
            path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path, **kwargs)

    def update_pin_chunk(self, chunk_address: str, **kwargs):
        method = "PUT"
        path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path, **kwargs)

    def delete_pin_chunk(self, chunk_address: str, **kwargs):
        method = "DELETE"
        path = "/pin/chunks/%s" % ChunkAddress(chunk_address)
        return self.call_request(method, path, **kwargs)

    def create_pin_bytes(self, bytes_address: str, **kwargs):
        method = "POST"
        path = "/pin/bytes/%s" % BytesAddress(bytes_address)
        return self.call_request(method, path, **kwargs)

    def delete_pin_bytes(self, bytes_address: str, **kwargs):
        method = "DELETE"
        path = "/pin/bytes/%s" % BytesAddress(bytes_address)
        return self.call_request(method, path, **kwargs)

    def create_pin_files(self, file_address: str, **kwargs):
        method = "POST"
        path = "/pin/files/%s" % FileAddress(file_address)
        return self.call_request(method, path, **kwargs)

    def delete_pin_files(self, file_address: str, **kwargs):
        method = "POST"
        path = "/pin/files/%s" % FileAddress(file_address)
        return self.call_request(method, path, **kwargs)

    def create_pin_collection(self, collection_address: str, **kwargs):
        method = "POST"
        path = "/pin/bzz/%s" % CollectionAddress(collection_address)
        return self.call_request(method, path, **kwargs)

    def delete_pin_collection(self, collection_address: str, **kwargs):
        method = "POST"
        path = "/pin/bzz/%s" % CollectionAddress(collection_address)
        return self.call_request(method, path, **kwargs)

    def send_pss(self, topic: str, targets: str, **kwargs):
        method = "POST"
        path = "/pss/send/{topic}/{targets}".format(topic=topic, targets=targets)
        return self.call_request(method, path, **kwargs)

    def subscribe_pss(self, topic: str, **kwargs):
        method = "GET"
        path = "/pss/subscribe/{topic}".format(topic=topic)
        return self.call_request(method, path, **kwargs)

    def create_single_owner_chunk(self, owner: str, _id: str, sig: str, **kwargs):
        method = "POST"
        path = "/soc/{owner}/{id}?{query}".format(
            owner=OwnerAddress(owner),
            id=IdAddress(_id),
            query=urlencode({"sig": sig})
        )
        return self.call_request(method, path, **kwargs)

    def create_feed(self, owner: str, topic: str, swarm_pin: bool, _type: str = "sequence", **kwargs):
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
        return self.call_request(method, path, headers=headers, **kwargs)

    def get_feed(self, owner: str, topic: str, at: int = None, _type: str = "sequence", **kwargs):
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
        return self.call_request(method, path, **kwargs)
