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

dc52 = debug_api.Client(url="http://192.168.1.52:1635", is_raise=False)
dc59 = debug_api.Client(url="http://192.168.1.59:1635", is_raise=False)
ac = api.Client(url="http://192.168.1.52:1633")


def p(m):
    print("-----%s-----" % m)


# print(dir(dc))
# p("get_balances")
# pprint(dc.get_balances())
# p("get_balances|address")
# print(dc.get_balances('bbcbbac81f89966a90118584a3ec2f75ee33661f02cf1fa6c3e277767be20c5a'))
# p("get_addresses")
# print(dc.get_addresses())
# p("get_blocklist")
# print(dc.get_blocklist())
# p("get_peers")
# pprint(dc.get_peers())
# print("remove_peer")
# print(dc.remove_peer('ffe76aff04aaad1aaacf952210691a005167185b794b225d070f18ad8cbba6cf'))
# print(dc.connect_peer('/ip4/127.0.0.1/tcp/1634/p2p/16Uiu2HAmUdCRWmyQCEahHthy7G4VsbBQ6dY9Hnk79337NfadKJEs'))
# print(dc.get_topology())
# p("get_welcome_message")
# print(dc.get_welcome_message())
# print(dc.set_welcome_message("x2x4-%s" % int(time())))
# print(dc.get_welcome_message())
# p("get_consumed")
# print(dc.get_consumed())
# p("get_consumed|bfe8e827ec2fa0441ea71ceb3cd93f6656955eec4a66725ab20d0515998e2254")
# print(dc.get_consumed("bfe8e827ec2fa0441ea71ceb3cd93f6656955eec4a66725ab20d0515998e2254"))


# p("get_chequebook_address")
# print(dc.get_chequebook_address())

# p("get_chequebook_balance")
# print(dc.get_chequebook_balance())

# p("get_chequebook_cheque")
# print(dc.get_chequebook_cheque())

p('52所有未兑现的支票')
pprint(dc52.list_all_uncashed())

p('59所有未兑现的支票')
pprint(dc59.list_all_uncashed())


print('52兑现所有支票，金额>1000')
print(dc52.cashout())

print('59兑现所有支票，金额>1000')
print(dc59.cashout())

# print('查看支票余额')
# print(dc.get_chequebook_balance())

# print('提现100000')
# print(dc.do_chequebook_withdraw(100000))

# sleep(10)

# print('查看支票余额')
# print(dc.get_chequebook_balance())

p('52连接状态')
print("Total peers: %s" % len(dc52.get_peers().data['peers']))
print("Negative peers: %s" % len([x for x in dc52.get_balances().data['balances'] if x['balance'] <= 0]))

p('59连接状态')
print("Total peers: %s" % len(dc59.get_peers().data['peers']))
print("Negative peers: %s" % len([x for x in dc59.get_balances().data['balances'] if x['balance'] <= 0]))


