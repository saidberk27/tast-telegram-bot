import time
from threading import Timer
def display(msg):
    print(msg)

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
        print("done")

timer = RepeatTimer(1, display,["mesajj"])
timer.start()
time.sleep(4)
print("threading finishing...")
timer.cancel()