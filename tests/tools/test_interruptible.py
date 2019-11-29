from threading import Thread, Event
from unittest import TestCase
import time

from GTG.tools.interruptible import interruptible, _cancellation_point


class TestInterruptibleDecorator(TestCase):

    def setUp(self):
        self.quit_condition = False
        self.thread_started = Event()

    @interruptible
    def never_ending(self, cancellation_point):
        self.thread_started.set()
        while True:
            time.sleep(0.01)
            cancellation_point()

    def test_interruptible_decorator(self):
        """ Tests for the @interruptible decorator. """
        thread = Thread(target=self.never_ending, args=(
            lambda: _cancellation_point(lambda: self.quit_condition),))
        thread.start()

        # Wait until thread comes to live
        self.thread_started.wait()

        # Ask to it to quit within 20ms
        self.quit_condition = True
        time.sleep(0.02)

        # Thread is finished
        self.assertFalse(thread.is_alive())
