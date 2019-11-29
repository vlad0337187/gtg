

class Borg(object):
    """
    This pattern ensures that all instances of a particular class share
    the same state (just inherit this class to have it working)
    """

    _borg_state = {}

    def __init__(self):
        self.__dict__ = self._borg_state
