"""Reusable logging configuration.

GTG modules and plugins that wish to use logging should import the Log object::

  from GTG.tools.logger import Log

...and target it with debug or info messages::

  Log.debug('Something has gone terribly wrong!')

"""
import logging


class Debug(object):
    """Singleton class that acts as interface for GTG's logger"""

    def __init__(self):
        """ Configure the GTG logger """
        # If we already have a logger, we keep that
        if not hasattr(Debug, "__logger"):
            self.__init_logger()
        # Shouldn't be needed, but the following line makes sure that
        # this is a Singleton.
        self.__dict__['_Debug__logger'] = Debug.__logger
        self.debugging_mode = False

    def __init_logger(self):
        Debug.__logger = logging.getLogger('gtg_logger')
        # set a stream handler for debugging
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - " +
                                      "%(module)s:%(funcName)s:%(lineno)d - " +
                                      "%(message)s")
        ch.setFormatter(formatter)
        Debug.__logger.addHandler(ch)

    def __getattr__(self, attr):
        """ Delegates to the real logger """
        return getattr(Debug.__logger, attr)

    def __setattr__(self, attr, value):
        """ Delegates to the real logger """
        return setattr(Debug.__logger, attr, value)

    def set_debugging_mode(self, value):
        self.debugging_mode = value

    def is_debugging_mode(self):
        return self.debugging_mode

# The singleton itself
Log = Debug()
