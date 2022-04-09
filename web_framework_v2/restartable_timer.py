from threading import Timer


class RestartableTimer(object):
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.timer = Timer(self.interval, self.function)

    def run(self):
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.interval, self.function)
        self.timer.start()

    def cancel(self):
        self.timer.cancel()
        self.timer = None
