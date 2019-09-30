import sys
from os.path import dirname, realpath, join

if getattr(sys, 'frozen', False):
    resource_dir = join(sys._MEIPASS, "resources")
else:
    resource_dir = dirname(realpath(__file__))


def get_resource(name):
    return join(resource_dir, name)
