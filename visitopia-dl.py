# -*- coding: utf-8 -*-
# author: cgcel


import getopt
import sys

from visitopia import VISTOPIA


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:v", ["help", "url="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print("""使用方法:
    python visitopia-dl.py [options]
参数:
    -h | --help 获取帮助
    -u | --url=<节目链接>""")
            sys.exit()
        elif o in ("-u", "--url"):
            url = a
            VISTOPIA().download_all(url=url)
        else:
            assert False, "unhandled option"


if __name__ == '__main__':
    main()
