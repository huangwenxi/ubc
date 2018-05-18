import threading
class Timer(object):

    def __init__(self, time,fun_timer):
        self.fun_timer = fun_timer
        self.time = time

    def function(self):
        timer = threading.Timer(self.time, self.fun_timer)
        timer.start()

    def run(self):
        timer = threading.Timer(self.time, self.function())
        timer.run()

