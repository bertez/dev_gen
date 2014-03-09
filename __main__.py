import os
import sys


class DevGenerator(object):
    def __init__(self, name, cvs_url):
        print 'iniciando: {0}, {1}'.format(name, cvs_url=None)

if __name__ == '__main__':
    d = DevGenerator('pirolas', 'git-url')
