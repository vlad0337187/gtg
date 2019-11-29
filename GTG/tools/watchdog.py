import threading


class Watchdog(object):
    '''
    a simple thread-safe watchdog.
    usage::
        with Watchdod(timeout, error_function):
            #do something
    '''

    def __init__(self, timeout, error_function):
        '''
        Just sets the timeout and the function to execute when an error occours

        @param timeout: timeout in seconds
        @param error_function: what to execute in case the watchdog timer
                               triggers
        '''
        self.timeout = timeout
        self.error_function = error_function

    def __enter__(self):
        '''Starts the countdown'''
        self.timer = threading.Timer(self.timeout, self.error_function)
        self.timer.start()

    def __exit__(self, type, value, traceback):
        '''Aborts the countdown'''
        try:
            self.timer.cancel()
        except:
            pass
        if value is None:
            return True
        return False
