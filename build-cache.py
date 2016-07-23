
# *nix environments only.

import os

import logging

from wurst_parser import WurstParser

LIB_FOLDER = "./WurstScript/Wurstpack/wurstscript/lib/"


def parse_file(root, file):
    fullname  = "/".join([root, file])
    p         = WurstParser(fullname, LIB_FOLDER).run()
    for line in p:
        print line
    return


def parse_files(root, files):
    for file in files:
        parse_file(root, file)
    return


# Entry point.
if __name__ == "__main__":
    logging.basicConfig(filename='build-cache.log', level=logging.DEBUG)
    for root, dirs, files in os.walk(LIB_FOLDER):
        parse_files(root, files)
