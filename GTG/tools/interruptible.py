'''
Utils to stop and quit gracefully a thread, issuing the command from
another one
'''


class Interrupted(Exception):
    '''Exception raised when a thread should be interrupted'''
    pass


def interruptible(fn):
    '''
    A decorator that makes a function interruptible. It should be applied only
    to the function which is the target of a Thread object.
    '''

    def new(*args):
        try:
            return fn(*args)
        except Interrupted:
            return
    return new


def _cancellation_point(test_function):
    '''
    This function checks a test_function and, if it evaluates to True, makes
    the thread quit (similar to pthread_cancel() in C)
    It starts with a _ as it's mostly used in a specialized form, as::
        cancellation_point = functools.partial(_cancellation_point,
                                               lambda: quit_condition == True)

    @param test_function: the function to test before cancelling
    '''
    if test_function():
        raise Interrupted
