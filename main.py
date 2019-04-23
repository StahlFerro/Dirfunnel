from __future__ import print_function
import sys
import random
import string

import zerorpc

from pysrc.controller import list_dir


class API(object):

    def list_directories(self):
        docs = list_dir()
        print(docs)
        return docs


def parse_port():
    return 4242


def main():
    address = f"tcp://127.0.0.1:{parse_port()}"
    server = zerorpc.Server(API())
    server.bind(address)
    print(f"Start running on {address}")
    print(server.run())


if __name__ == "__main__":
    main()