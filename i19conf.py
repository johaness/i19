import sys
from os import path as osp


def main():
    print osp.join(osp.abspath(osp.dirname(__file__)), sys.argv[1])

