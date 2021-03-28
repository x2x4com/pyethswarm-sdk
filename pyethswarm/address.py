#!/usr/bin/env python3
# encoding: utf-8
import re


class AddressError(Exception):
    pass


class Address(object):
    regs = [re.compile(r"^[A-Fa-f0-9]{64}$")]

    def __init__(self, address: str):
        is_match = False
        for reg in self.regs:
            if reg.match(address):
                is_match = True
        if not is_match:
            raise AddressError("Address not match one of %s" % [r.pattern for r in self.regs])
        self.address = address

    def __str__(self):
        return self.address

    def __repr__(self):
        return self.address


class PeerAddress(Address):
    pass


class ContentAddress(Address):
    regs = [
        re.compile(r"^[A-Fa-f0-9]{64}$"),
        re.compile(r"^[A-Fa-f0-9]{128}$"),
        re.compile(r"^[A-Za-z0-9]+\.[A-Za-z0-9]+$")
    ]


class ChunkAddress(ContentAddress):
    pass


class BytesAddress(Address):
    pass


class FileAddress(Address):
    pass


class CollectionAddress(Address):
    pass


class IdAddress(Address):
    regs = [re.compile(r"^([A-Fa-f0-9]+)$")]


class OwnerAddress(Address):
    regs = [re.compile(r"^[A-Fa-f0-9]{40}$")]
