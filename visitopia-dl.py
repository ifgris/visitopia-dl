# -*- coding: utf-8 -*-
# author: cgcel

from visitopia import VISTOPIA


def main():
    url = input("Input url: ")
    VISTOPIA().download_articles(url=url)


if __name__ == '__main__':
    main()
