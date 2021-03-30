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
from sys import argv

dc52 = debug_api.Client(url="http://192.168.1.52:1635", is_raise=False)
dc59 = debug_api.Client(url="http://192.168.1.59:1635", is_raise=False)
ac = api.Client(url="http://192.168.1.52:1633")

is_clean = False

try:
    if argv[1] in ['true', '1', 'clean', 'True']:
        is_clean = True
except IndexError:
    pass


def p(m):
    print("-----%s-----" % m)


def pp(m):
    pprint(m, sort_dicts=False)


def negative_balances_peers(dc: debug_api.Client):
    _neative_peers = [x for x in dc.get_balances().data['balances'] if x['balance'] < 0]
    _all_peers = [_p['address'] for _p in dc.get_peers().data['peers']]
    _connected_negaive_peers = [y for y in _neative_peers if y['peer'] in _all_peers]
    return _connected_negaive_peers


def connected_peers_balances(dc: debug_api.Client):
    _all_peers = [_p['address'] for _p in dc.get_peers().data['peers']]
    _connected_peers_balances = list()
    for _p in _all_peers:
        balance = dc.get_balances(_p).data
        if 'balance' in balance:
            _connected_peers_balances.append(balance)
        else:
            _connected_peers_balances.append({'peer': _p, 'balance': -1})
    return _connected_peers_balances


def disconnect_peers(dc: debug_api.Client, peers):
    for _p in peers:
        pp(dc.remove_peer(_p).to_dict())


# p('52余额为负数的节点已经连接的节点')
_nbp_52 = [x for x in dc52.get_balances().data['balances'] if x['balance'] < 0]
# pprint(_nbp_52)

p('52节点余额')
pp(connected_peers_balances(dc52))


# p('59余额为负数的节点已经连接的节点')
_nbp_59 = [x for x in dc59.get_balances().data['balances'] if x['balance'] < 0]
# pprint(_nbp_59)


p('59节点余额')
pp(connected_peers_balances(dc59))

if is_clean:
    p('移除52负数节点')
    _cpb_52 = [x['peer'] for x in connected_peers_balances(dc52) if x['balance'] <= 0]
    disconnect_peers(dc52, [__p['peer'] for __p in _nbp_52])
    disconnect_peers(dc52, _cpb_52)

    p('移除59负数节点')
    _cpb_59 = [x['peer'] for x in connected_peers_balances(dc59) if x['balance'] <= 0]
    disconnect_peers(dc59, [__p['peer'] for __p in _nbp_59])
    disconnect_peers(dc59, _cpb_59)


p('52连接信息')
print("Total peers: %s" % len(dc52.get_peers().data['peers']))
print("Negative peers: %s" % len(_nbp_52))


p('59连接信息')
print("Total peers: %s" % len(dc59.get_peers().data['peers']))
print("Negative peers: %s" % len(_nbp_59))




