#!/usr/bin/env python
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

from pprint import pprint
from pyethswarm import api
from time import time

ac = api.Client("http://192.168.1.52:1633")


# muscle_doge.png 52131e77eca88d99f8b96b7094ada330b9fdf0d480f05a4e70d7646a5fbf4180

# exist
# pprint(ac.get_files('52131e77eca88d99f8b96b7094ada330b9fdf0d480f05a4e70d7646a5fbf4180'))

# not exist
# pprint(ac.get_files('52131e77eca88d99f8b96b7094ada330b9fdf0d480f05a4e70d7646a5fbf4181'))


# with open('muscle_doge.png', 'rb') as f:
#    now = int(time())
#    pprint(ac.upload_files(file_name="md_%s" % now, file_bin=f.read()))

# md_1617092668 9389bf072f14ec29f9c393a7f4d467a4045c4e3a150567902ee53c2d547d5b5e
# pprint(ac.get_files('9389bf072f14ec29f9c393a7f4d467a4045c4e3a150567902ee53c2d547d5b5e'))
# pprint(ac.get_files('52131e77eca88d99f8b96b7094ada330b9fdf0d480f05a4e70d7646a5fbf4180'))

# 重复的文件与文件名可以多次添加，总返回第一次的哪个(文件不变的情况下)
# with open('muscle_doge.png', 'rb') as f:
#     pprint(ac.upload_files(file_name="muscle_doge.png", file_bin=f.read(), content_type='image/png'))
    # 9cc8317473e3ed6cc5400cb290a4c3a3bc423a2d5f2877268971b13f01a1dbd1
    # 9cc8317473e3ed6cc5400cb290a4c3a3bc423a2d5f2877268971b13f01a1dbd1


# tar文件上传测试
with open('site.tar', 'rb') as t:
    _b = t.read()
    # print(_b)
    pprint(ac.upload_collection(collection_bin=_b, timeout=1200))
    # 2640678ea308036c080ceba64e0f23bef21baeba999614413d620ec2cb70d868

