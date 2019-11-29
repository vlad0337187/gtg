""" Communicate with Network Manager """

import gi
gi.require_version('NMClient', '1.0')
gi.require_version('NetworkManager', '1.0')
from gi.repository import NetworkManager, NMClient


def is_connection_up():
    """ Returns True if GTG can access the Internet """
    state = NMClient.Client().get_state()
    return state == NetworkManager.State.CONNECTED_GLOBAL

if __name__ == "__main__":
    print("is_connection_up() == %s" % is_connection_up())
