#!/usr/bin/env python3
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION:
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (),
#      COMPANY:
#      VERSION:  1.0
#      CREATED:
#     REVISION:  ---
# ===============================================================================

from pyethswarm import debug_api, api
from time import sleep, time
from pprint import pprint
from collections import OrderedDict

dc = debug_api.Client(url="http://192.168.1.52:1635", is_raise=False)
ac = api.Client(url="http://192.168.1.52:1633")


def p(m):
    print("-----%s-----" % m)


def negative_balances_peers():
    _neative_peers = [x for x in dc.get_balances()['balances'] if x['balance'] <= 0]
    _all_peers = [_p['address'] for _p in dc.get_peers()['peers']]
    _connected_negaive_peers = [y for y in _neative_peers if y['peer'] in _all_peers]
    return _connected_negaive_peers


def connected_peers_balances():
    _all_peers = [_p['address'] for _p in dc.get_peers()['peers']]
    _connected_peers_balances = list()
    for _p in _all_peers:
        balance = dc.get_balances(_p)
        if 'balance' in balance:
            _connected_peers_balances.append(balance)
        else:
            _connected_peers_balances.append({'peer': _p, 'balance': 0})
    return _connected_peers_balances


def disconnect_peers(peers):
    for _p in peers:
        pprint(dc.remove_peer(_p))


p('列出余额为负数的节点已经连接的节点')
_nbp = [x for x in dc.get_balances()['balances'] if x['balance'] <= 0]
pprint(_nbp)

p('当前所有节点余额')
pprint(connected_peers_balances())

print("Total peers: %s" % len(dc.get_peers()['peers']))
print("Negative peers: %s" % len(_nbp))

# p('移除负数节点')
# _cpb = [x['peer'] for x in connected_peers_balances() if x['balance'] <= 0]
# disconnect_peers([__p['peer'] for __p in _nbp])
# disconnect_peers(_cpb)




