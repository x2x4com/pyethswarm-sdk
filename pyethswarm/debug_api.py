#!/usr/bin/env python3
# encoding: utf-8
from urllib.parse import urlencode, quote
from .common import ClientBase, RetType, ApiError, Headers, ContentType
from .address import PeerAddress, ChunkAddress, MultiAddress, TxHash
from typing import List, Union, Dict


class Client(ClientBase):
    __version = "1.0.0"

    def __init__(self, url: str = "http://localhost:1635", is_raise=True):
        super().__init__(url, self.__version)
        self.is_raise = is_raise

    def get_addresses(self):
        method = "GET"
        path = "/addresses"
        return self.call_request(method, path)

    def get_blocklist(self):
        method = "GET"
        path = "/blocklist"
        return self.call_request(method, path)

    def get_peers(self):
        method = "GET"
        path = "/peers"
        return self.call_request(method, path)

    def remove_peer(self, peer_address: PeerAddress):
        method = "DELETE"
        path = "/peers/%s" % peer_address
        return self.call_request(method, path)

    def connect_peer(self, address: MultiAddress):
        method = "POST"
        path = "/connect/%s" % quote(str(address))
        return self.call_request(method, path)

    def ping_peer(self, address: PeerAddress):
        method = "POST"
        path = "/pingpong/{peer_id}".format(peer_id=address)
        return self.call_request(method, path)

    def get_topology(self):
        method = "GET"
        path = "/topology"
        return self.call_request(method, path)

    def get_welcome_message(self):
        method = "GET"
        path = "/welcome-message"
        return self.call_request(method, path)

    def set_welcome_message(self, msg: str):
        method = "POST"
        path = "/welcome-message"
        headers = Headers()
        headers['content-type'] = ContentType.JSON
        data = {
            "welcome_message": msg
        }
        return self.call_request(method, path, json=data, headers=headers)

    def get_balances(self, address: Union[PeerAddress, None]=None):
        if address is None:
            path = "/balances"
        else:
            path = "/balances/%s" % address
        method = "GET"
        return self.call_request(method, path)

    def get_consumed(self, address: Union[PeerAddress, None]=None):
        method = "GET"
        if address is None:
            path = "/consumed"
        else:
            path = "/consumed/%s" % address
        return self.call_request(method, path)

    def get_chequebook_address(self):
        method = "GET"
        path = "/chequebook/address"
        return self.call_request(method, path)
    
    def get_chequebook_balance(self):
        method = "GET"
        path = "/chequebook/balance"
        return self.call_request(method, path)

    def get_chequebook_cashout(self, peer_id: PeerAddress):
        method = "GET"
        path = "/chequebook/cashout/%s" % peer_id
        return self.call_request(method, path)

    def do_chequebook_cashout(self, peer_id: PeerAddress, gas_price_gwei: int=1):
        method = "POST"
        path = "/chequebook/cashout/%s" % peer_id
        # todo 需要测试确认
        headers = Headers({
            "gas-price": gas_price_gwei * 10**9,
            "gas-limit": 6000000
        })
        return self.call_request(method, path, headers=headers)

    def get_chequebook_cheque(self, peer_id: Union[PeerAddress, None]=None):
        method = "GET"
        if peer_id is None:
            path = "/chequebook/cheque"
        else:
            path = "/chequebook/cheque/%s" % peer_id
        return self.call_request(method, path)

    def do_chequebook_deposit(self, amount: int, gas_price_gwei: int=1):
        method = "POST"
        query_params = urlencode({
            "amount": amount
        })
        headers = Headers({
            "gas-price": gas_price_gwei * 10 ** 9,
        })
        path = "/chequebook/deposit?%s" % query_params
        return self.call_request(method, path, headers=headers)

    def do_chequebook_withdraw(self, amount: int, gas_price_gwei: int=1):
        method = "POST"
        # available_balance = self.get_chequebook_balance()['availableBalance']
        available_balance = self.get_chequebook_balance().to_dict().get('data').get('availableBalance')
        if available_balance is None or amount >= available_balance:
            print("Insufficient balance, or can not get balance")
            return
        query_params = urlencode({
            "amount": amount
        })
        headers = Headers({
            "gas-price": gas_price_gwei * 10 ** 9,
        })
        path = "/chequebook/withdraw?%s" % query_params
        return self.call_request(method, path, headers=headers)

    def get_chunks(self, chunk_address: ChunkAddress):
        # Check if chunk at address exists locally
        method = "GET"
        path = "/chunks/%s" % chunk_address
        return self.call_request(method, path)

    def delete_chunks(self, chunk_address: ChunkAddress):
        # Delete a chunk from local storage
        method = "DELETE"
        path = "/chunks/%s" % chunk_address
        return self.call_request(method, path)

    # status

    def get_reserve_state(self):
        method = "GET"
        path = '/reservestate'
        return self.call_request(method, path)

    def get_chain_state(self):
        method = "GET"
        path = '/chainstate'
        return self.call_request(method, path)

    def get_health(self):
        method = "GET"
        path = "/health"
        return self.call_request(method, path)

    def get_readiness(self):
        method = "GET"
        path = "/readiness"
        return self.call_request(method, path)

    def get_settlements(self, peer_address: Union[PeerAddress, None]=None):
        method = "GET"
        if peer_address is None:
            path = "/settlements"
        else:
            path = "/settlements/%s" % peer_address
        return self.call_request(method, path)

    def get_time_settlements(self):
        method = "GET"
        path = "/timesettlements"
        return self.call_request(method, path)

    def get_tags(self, uid: int):
        method = "GET"
        path = "/tags/%s" % uid
        return self.call_request(method, path)

    def get_transaction(self, tx_hash: Union[TxHash, None]=None):
        method = "GET"
        if tx_hash is None:
            path = "/transaction"
        else:
            path = "/transaction/{tx_hash}".format(tx_hash=tx_hash)
        return self.call_request(method, path)

    # todo 先对比一下官方最新的cashout脚本
    # todo 下面这些方法需要在1.0.0上面测试，
    def uncashed_amount(self, peer: PeerAddress) -> int:
        """
        count uncashed amount

        Args:
            peer: peer address

        Returns: int

        """
        pd = self.get_chequebook_cheque(peer).data
        diff = 0
        # print("pd: %s" % pd)
        if pd is not None and 'lastreceived' in pd and pd['lastreceived'] is not None and 'payout' in pd[
            'lastreceived']:
            cumulative_payout = pd['lastreceived']['payout']
            if cumulative_payout is None or cumulative_payout == 0:
                # print("cumulative_payout: %s" % cumulative_payout)
                return diff
            _past_cashed_payout = self.get_chequebook_cashout(peer).data
            # print("_past_cashed_payout: %s" % _past_cashed_payout)
            if 'cumulativePayout' in _past_cashed_payout:
                cashed_payout = _past_cashed_payout['cumulativePayout']
                # print("cumulative_payout: %s" % cumulative_payout)
                # print("cashed_payout: %s" % cashed_payout)
                diff = cumulative_payout - cashed_payout
        return diff

    def list_all_uncashed(self) -> list:
        """
        Get all uncashed peers

        Returns: list(tuple(peer_id, cashed_payout))

        """
        peers = self.all_cheque_peers()
        uncashed_peers = list()
        for peer in peers:
            diff = self.uncashed_amount(peer)
            if diff > 0:
                uncashed_peers.append((peer, diff))
        return uncashed_peers

    def all_cheque_peers(self) -> list:
        """
        Get all cheque peers

        Returns: list(peer)

        """
        data = self.get_chequebook_cheque().data
        return [pp['peer'] for pp in data['lastcheques']]

    def cashout(self, peer: str=None, min_amount: int=1000):
        """
        Cashout

        Args:
            peer: if peer not defined, cashout all peers
            min_amount: cashout > min_amount and start

        Returns:

        """
        if peer is None:
            peers = self.all_cheque_peers()
        else:
            peers = [PeerAddress(peer)]

        cashed_list = list()
        for _peer in peers:
            diff = self.uncashed_amount(_peer)
            if diff > 0 and diff > min_amount:
                _cash_out = self.do_chequebook_cashout(_peer).data
                cashed_list.append((_peer, _cash_out))

        return cashed_list

