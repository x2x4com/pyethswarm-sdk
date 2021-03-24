#!/usr/bin/env python3
# encoding: utf-8
from urllib.parse import urlencode
from .common import ClientBase, RetType, ApiError, Headers


class Client(ClientBase):
    __version = "0.5.2"

    def __init__(self, url: str = "http://localhost:1635"):
        super().__init__(url, self.__version)

    def __call_request(self, method, path, **kwargs):
        ret = self._request(method, path, **kwargs)
        if ret.code != RetType.OK:
            raise ApiError("DEBUG_API", method, path, ret.code, ret.msg)
        return ret.data

    def get_balances(self, address=None):
        if address is None:
            path = "/balances"
        else:
            path = "/balances/%s" % address
        method = "GET"
        return self.__call_request(method, path)

    def get_consumed(self, address=None):
        method = "GET"
        if address is None:
            path = "/consumed"
        else:
            path = "/consumed/%s" % address
        return self.__call_request(method, path)

    def get_chequebook_address(self):
        method = "GET"
        path = "/chequebook/address"
        return self.__call_request(method, path)
    
    def get_chequebook_balance(self):
        method = "GET"
        path = "/chequebook/balance"
        return self.__call_request(method, path)

    def get_chequebook_cashout(self, peer_id):
        method = "GET"
        path = "/chequebook/cashout/%s" % peer_id
        return self.__call_request(method, path)

    def post_chequebook_cashout(self, peer_id, gas_price_gwei=1):
        method = "POST"
        path = "/chequebook/cashout/%s" % peer_id
        # 官方的cashout脚本并没有使用这个头，需要测试确认
        headers = Headers({
            "gas-price": gas_price_gwei * 10**9,
            "gas-limit": 6000000
        })
        return self.__call_request(method, path)

    def get_chequebook_cheque(self, peer_id=None):
        method = "GET"
        if peer_id is None:
            path = "/chequebook/cheque"
        else:
            path = "/chequebook/cheque/%s" % peer_id
        return self.__call_request(method, path)

    def post_chequebook_deposit(self, amount: int):
        method = "POST"
        amount = amount * 10**16
        query_params = urlencode({
            "amount": amount
        })
        path = "/chequebook/deposit?%s" % query_params
        return self.__call_request(method, path)

    def post_chequebook_withdraw(self, amount: int):
        method = "POST"
        amount = amount * 10**16
        query_params = urlencode({
            "amount": amount
        })
        path = "/chequebook/withdraw?%s" % query_params
        return self.__call_request(method, path)

    def get_chunks(self, chunk_address):
        method = "GET"
        path = "/chunks/%s" % chunk_address
        return self.__call_request(method, path)

    def delete_chunks(self, chunk_address):
        method = "DELETE"
        path = "/chunks/%s" % chunk_address
        return self.__call_request(method, path)

    def get_health(self):
        method = "GET"
        path = "/health"
        return self.__call_request(method, path)

    def get_readiness(self):
        method = "GET"
        path = "/readiness"
        return self.__call_request(method, path)

    def get_settlements(self, peer_address=None):
        method = "GET"
        if peer_address is None:
            path = "/settlements"
        else:
            path = "/settlements/%s" % peer_address
        return self.__call_request(method, path)

    def get_tags(self, uid: int):
        method = "GET"
        path = "/tags/%s" % uid
        return self.__call_request(method, path)



