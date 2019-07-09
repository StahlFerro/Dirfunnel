from __future__ import print_function
import sys
import random
import string

import zerorpc

from pybrain.orm import add_update_directory, freeze_directories, list_directories, remove_directory


class API(object):

    def get_directories(self):
        docs = list_directories()
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

