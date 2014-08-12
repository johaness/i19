import sys
from os import path as osp


def main():
    """
    Usage: i19conf FILENAME

      Returns the absolute path to FILENAME inside the i19 module.
    """
    assert len(sys.argv) > 1, main.__doc__

    modpath = osp.abspath(osp.dirname(__file__))
    fullpath = osp.join(modpath, sys.argv[1])
    if not osp.exists(fullpath):
        sys.exit('"{}" not found in "{}".'.format(sys.argv[1], modpath))
    print(fullpath)


if __name__ == '__main__':
    main()
