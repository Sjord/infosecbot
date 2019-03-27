import signal
import sys


class Timeout:
    def __init__(self, timeout):
        self.timeout = timeout

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(self.timeout)
        return self

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

    def alarm_handler(self, ignum, frame):
        signal.alarm(self.timeout)
        raise TimeoutError()
