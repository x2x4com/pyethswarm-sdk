#!/usr/bin/env python3
# encoding: utf-8
from urllib.parse import urlencode
from .common import ClientBase, Headers, ContentType, RetType
from .address import *
from time import time
import os
from hashlib import sha256
import tarfile


class Client(ClientBase):
    __version = "1.0.0"

    def __init__(self, url: str = 'http://localhost:1633', is_raise=True):
        super().__init__(url, self.__version)
        self.is_raise = is_raise

    def create_bytes(self, swarm_postage_batch_id: Address, swarm_tag: int, swarm_pin: bool, swarm_encrypt: bool, **kwargs):
        method = "POST"
        path = "/bytes"
        headers = Headers({
            # 预先生成的tag
            "swarm-tag": swarm_tag,
            # 是否持久化
            "swarm-pin": swarm_pin.__str__().lower(),
            "swarm-encrypt": swarm_encrypt,
            "swarm-postage-batch-id": swarm_postage_batch_id
        })
        return self.call_request(method, path, headers=headers, **kwargs)

    def get_bytes(self, reference: str, **kwargs):
        method = "GET"
        path = "/bytes/%s" % ContentAddress(reference)
        return self.call_request(method, path, **kwargs)

    def get_chunks(self, reference: str, targets: str = None, **kwargs):
        method = "GET"
        if targets is None:
            path = "/chunks/%s" % ChunkAddress(reference)
        else:
            query_params = urlencode({
                "targets": targets
            })
            path = "/chunks/{}?{}".format(ChunkAddress(reference), query_params)
        return self.call_request(method, path, **kwargs)

    def create_chunks(self, swarm_postage_batch_id: Address, string_bin: bytes, swarm_tag: int, swarm_pin: bool, **kwargs):
        method = "POST"
        path = "/chunks"
        headers = Headers({
            "swarm-tag": swarm_tag,
            "swarm-pin": swarm_pin.__str__().lower(),
            "swarm-postage-batch-id": swarm_postage_batch_id
        })
        headers['content-type'] = ContentType.OCTETSTEAM
        return self.call_request(method, path, headers=headers, data=string_bin, **kwargs)

    # def get_files(self, reference: str, **kwargs):
    #     """
    #     Get file via reference(Content Address)
    #
    #     Args:
    #         reference: Content Address
    #
    #     Returns:
    #         existed: return dict({"name": str, "content_type": str, "msg": str, "data": base64encode(byte) })
    #         not existed: RetType object
    #
    #     """
    #     method = "GET"
    #     path = "/files/%s" % ContentAddress(reference)
    #     ret = self.call_request(method, path, stream=True, **kwargs)
    #     if ret.code != 200:
    #         return ret
    #     _ret_data = ret.data
    #     _reg = re.compile(r'filename="(.*)"').findall(_ret_data['headers']['Content-Disposition'])
    #     msg = "OK"
    #     if len(_reg) > 0:
    #         file_name = _reg[0]
    #     else:
    #         file_name = _ret_data['headers']['Content-Disposition']
    #         msg = "Can not find file name, use Content-Disposition instead"
    #     return {
    #         "name": file_name,
    #         "content_type": _ret_data['headers']['Content-Type'],
    #         "msg": msg,
    #         "data": _ret_data['raw']
    #     }

    # def upload_files(self,
    #                  file_name: str,
    #                  content_type: str,
    #                  file_bin: bytes,
    #                  swarm_tag: int = None,
    #                  swarm_pin: bool = False,
    #                  swarm_encrypt: bool = False,
    #                  **kwargs
    #                  ):
    #     """
    #     Upload file for v0.5.2
    #
    #     Args:
    #         file_name: file name
    #         content_type:  file type
    #         file_bin:  file byte
    #         swarm_tag:  tag id
    #         swarm_pin:  bool default false
    #         swarm_encrypt: bool default false
    #
    #    Returns:
    #        ok: return dict({"name": str, "reference": str})
    #        error: RetType object
    #
    #    """
    #     method = "POST"
    #     path = "/files?%s" % urlencode({"name": file_name})
    #     if swarm_tag is not None:
    #         headers = Headers({
    #             "swarm-tag": swarm_tag,
    #             "swarm-pin": swarm_pin.__str__().lower(),
    #             "swarm-encrypt": swarm_encrypt.__str__().lower()
    #         })
    #     else:
    #         headers = Headers({
    #             "swarm-pin": swarm_pin.__str__().lower(),
    #             "swarm-encrypt": swarm_encrypt.__str__().lower()
    #         })
    #     # headers['content-type'] = "multipart/form-data"
    #     headers['content-type'] = content_type
    #     # print(headers)
    #     ret = self.call_request(method, path, headers=headers, data=file_bin, **kwargs)
    #     if ret.code != 200:
    #         return ret
    #     return {
    #         "name": file_name,
    #         **ret.data
    #     }

    # def upload_collection(self,
    #                       collection_bin: bytes,
    #                       swarm_tag: int = None,
    #                       swarm_pin: bool = False,
    #                       swarm_encrypt: bool = False,
    #                       swarm_index_document: str = "index.html",
    #                       swarm_error_document: str = "error.html",
    #                       **kwargs
    #                       ):
    #     method = "POST"
    #     path = "/dirs"
    #     if swarm_tag is not None:
    #         headers = Headers({
    #             "swarm-tag": swarm_tag,
    #             "swarm-pin": swarm_pin.__str__().lower(),
    #             "swarm-encrypt": swarm_encrypt.__str__().lower(),
    #             "swarm-index-document": swarm_index_document,
    #             "swarm-error-document": swarm_error_document
    #         })
    #     else:
    #         headers = Headers({
    #             "swarm-pin": swarm_pin.__str__().lower(),
    #             "swarm-encrypt": swarm_encrypt.__str__().lower(),
    #             "swarm-index-document": swarm_index_document,
    #             "swarm-error-document": swarm_error_document
    #         })
    #     headers['content-type'] = ContentType.XTAR
    #     return self.call_request(method, path, headers=headers, data=collection_bin, **kwargs)

    def upload_files(self,
                     swarm_postage_batch_id: Address,
                     content_type: str,
                     obj_target: str,
                     file_name: str = None,
                     swarm_tag: int = None,
                     swarm_pin: bool = False,
                     swarm_encrypt: bool = False,
                     swarm_collection: bool = False,
                     swarm_index_document: str = "index.html",
                     swarm_error_document: str = "error.html",
                     **kwargs
                     ):
        """
        Upload file # todo not finished

        Args:
            swarm_postage_batch_id: ID of Postage Batch that is used to upload data with
            content_type:  file type
            obj_target: str
            file_name: file name
            swarm_tag:  tag id
            swarm_pin:  bool default false
            swarm_encrypt: bool default false
            swarm_collection: bool default False,
            swarm_index_document: str default "index.html",
            swarm_error_document: str default "error.html",

       Returns:
           ok: return dict({"name": str, "reference": str})
           error: RetType object

       """
        method = "POST"

        headers = Headers({
            "swarm-postage-batch-id": swarm_postage_batch_id,
            "swarm-pin": swarm_pin.__str__().lower(),
            "swarm-encrypt": swarm_encrypt.__str__().lower(),
            "swarm-collection": swarm_collection.__str__().lower(),
            "swarm-index-document": swarm_index_document,
            "swarm-error-document": swarm_error_document
        })
        if swarm_tag is not None:
            headers.update({"swarm-tag": swarm_tag})
        if swarm_collection:
            path = "/bzz"
            # 这是collection，设置类型为x-tar，并读取目录打包
            headers['content-type'] = ContentType.XTAR
            if not os.path.isdir(obj_target):
                return RetType(
                    code=500,
                    data={},
                    msg="collection is true, require obj_target is folder"
                )
            now = time()
            tmp_name = "{}-{}.tar.gz".format(int(now), sha256(str(time()).encode()).hexdigest())
            with tarfile.open(tmp_name, 'w:gz') as tar:
                for root, _dir, files in os.walk(obj_target):
                    for file in files:
                        full_path = os.path.join(root, file)
                        tar.add(full_path)
            with open(tmp_name, 'rb') as _f:
                obj_bin = _f.read()
        else:
            path = "/bzz?%s" % urlencode({"name": file_name})
            headers['content-type'] = content_type
            if os.path.isdir(obj_target):
                return RetType(
                    code=500,
                    data={},
                    msg="collection is false, require obj_target is not folder"
                )
            with open(obj_target, 'rb') as _f:
                obj_bin = _f.read()

        # print(headers)
        ret = self.call_request(method, path, headers=headers, data=obj_bin, **kwargs)
        if ret.code != 200:
            return ret
        return {
            "name": file_name,
            **ret.data
        }

    def get_collection_index(self, reference: str, targets: str = None, **kwargs):
        """
        https://docs.ethswarm.org/docs/advanced/persistence#global-pinning

        :param reference:
        :param targets: global-pinning， 需要在节点打开global-pinning-enable标签，
        :return:
        """
        method = "GET"
        if targets is None:
            path = "/bzz/%s" % CollectionAddress(reference)
        else:
            path = "/bzz/%s?%s" % (CollectionAddress(reference), urlencode({"targets": targets}))
        return self.call_request(method, path, **kwargs)

    def get_collection_file(self, reference: str, file_path: str, targets: str = None, **kwargs):
        method = "GET"
        if targets is None:
            path = "/bzz/%s/%s" % (CollectionAddress(reference), file_path)
        else:
            path = "/bzz/%s/%s?%s" % (CollectionAddress(reference), file_path, urlencode({"targets": targets}))
        return self.call_request(method, path, **kwargs)

    def reupload_file(self, reference: CollectionAddress, **kwargs):
        method = "PATCH"
        path = "/bzz/%s" % CollectionAddress(reference)
        return self.call_request(method, path, **kwargs)

    def reupload_collection(self, reference: CollectionAddress, **kwargs):
        return self.reupload_file(reference, **kwargs)

    def get_tags(self, uid: str = None, offset: int = 0, limit: int = 100, **kwargs):
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

    def create_pin(self, reference: Address, **kwargs):
        method = "POST"
        path = "/pins/%s" % reference
        return self.call_request(method, path, **kwargs)

    def get_pin(self, reference: Address = None, **kwargs):
        method = "GET"
        if reference is None:
            path = "/pins"
        else:
            path = "/pins/%s" % reference
        return self.call_request(method, path, **kwargs)

    def update_pin(self, reference: Address, **kwargs):
        method = "PUT"
        path = "/pins/%s" % reference
        return self.call_request(method, path, **kwargs)

    def delete_pin(self, reference: Address, **kwargs):
        method = "DELETE"
        path = "/pins/%s" % reference
        return self.call_request(method, path, **kwargs)

    # def create_pin_bytes(self, bytes_address: str, **kwargs):
    #     method = "POST"
    #     path = "/pin/bytes/%s" % BytesAddress(bytes_address)
    #     return self.call_request(method, path, **kwargs)
    #
    # def delete_pin_bytes(self, bytes_address: str, **kwargs):
    #     method = "DELETE"
    #     path = "/pin/bytes/%s" % BytesAddress(bytes_address)
    #     return self.call_request(method, path, **kwargs)
    #
    # def create_pin_files(self, file_address: str, **kwargs):
    #     method = "POST"
    #     path = "/pin/files/%s" % FileAddress(file_address)
    #     return self.call_request(method, path, **kwargs)
    #
    # def delete_pin_files(self, file_address: str, **kwargs):
    #     method = "POST"
    #     path = "/pin/files/%s" % FileAddress(file_address)
    #     return self.call_request(method, path, **kwargs)
    #
    # def create_pin_collection(self, collection_address: str, **kwargs):
    #     method = "POST"
    #     path = "/pin/bzz/%s" % CollectionAddress(collection_address)
    #     return self.call_request(method, path, **kwargs)
    #
    # def delete_pin_collection(self, collection_address: str, **kwargs):
    #     method = "POST"
    #     path = "/pin/bzz/%s" % CollectionAddress(collection_address)
    #     return self.call_request(method, path, **kwargs)

    def send_pss(self, swarm_postage_batch_id: Address, topic: str, targets: str, recipient: str, **kwargs):
        method = "POST"
        path = "/pss/send/{topic}/{targets}?{query}".format(
            topic=topic,
            targets=targets,
            query=urlencode({"recipient": recipient})
        )
        headers = Headers({
            "swarm-postage-batch-id": swarm_postage_batch_id,
        })
        return self.call_request(method, path, headers=headers, **kwargs)

    def subscribe_pss(self, topic: str, **kwargs):
        method = "GET"
        path = "/pss/subscribe/{topic}".format(topic=topic)
        return self.call_request(method, path, **kwargs)

    def create_single_owner_chunk(self, owner: str, _id: str, sig: str, swarm_pin: bool = False, **kwargs):
        method = "POST"
        path = "/soc/{owner}/{id}?{query}".format(
            owner=OwnerAddress(owner),
            id=IdAddress(_id),
            query=urlencode({"sig": sig})
        )
        headers = Headers({
            "swarm-pin": swarm_pin.__str__().lower()
        })
        return self.call_request(method, path, headers=headers, **kwargs)

    def create_feed(self, swarm_postage_batch_id: Address, owner: str, topic: str, swarm_pin: bool, _type: str = "sequence", **kwargs):
        method = "POST"
        if _type not in ["sequence", "epoch"]:
            _type = "sequence"
        path = "/feeds/{owner}/{topic}?{query}".format(
            owner=OwnerAddress(owner),
            topic=IdAddress(topic),
            query=urlencode({"type": _type})
        )
        headers = Headers({
            "swarm-pin": swarm_pin.__str__().lower(),
            "swarm-postage-batch-id": swarm_postage_batch_id
        })
        return self.call_request(method, path, headers=headers, **kwargs)

    def get_feed(self, owner: str, topic: str, _at: int = None, _type: str = "sequence", **kwargs):
        method = "GET"
        if _type not in ["sequence", "epoch"]:
            _type = "sequence"
        if _at is None:
            _at = int(time())
        path = "/feeds/{owner}/{topic}?{query}".format(
            owner=OwnerAddress(owner),
            topic=IdAddress(topic),
            query=urlencode({"type": _type, "at": _at})
        )
        return self.call_request(method, path, **kwargs)

    def get_stamps(self, stamp_id: StampId = None, **kwargs):
        method = "GET"
        if stamp_id is None:
            path = "/stamps"
        else:
            path = "/stamps/{id}".format(id=stamp_id)
        return self.call_request(method, path, **kwargs)

    def buy_stamps(self, amount: int, depth: int = 16, gas_price_gwei: int=1, label: str = None, **kwargs):
        method = "POST"
        headers = Headers({
            "gas-price": gas_price_gwei * 10**9,
        })
        if depth < 16:
            depth = 16
        if label is None:
            path = "/stamps/{amount}/{depth}".format(amount=amount, depth=depth)
        else:
            path = "/stamps/{amount}/{depth}?{query}".format(
                amount=amount,
                depth=depth,
                query=urlencode({
                    "label": label
                })
            )

        return self.call_request(method, path, headers=headers, **kwargs)
