from threading import Thread
from time import sleep
import time

from flask import Flask


class Shutter(Thread):

    def __init__(self, interval, total_shots, press_time=0.1, focus_time=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.press_time = press_time
        self.focus_time = focus_time
        self.total_shots = total_shots
        self.remaining_shots = total_shots
        self.shots_taken = 0
        self.first_time = time.perf_counter()  # init based on perf_counter

    def run(self):

        while self.remaining_shots > 0:

            self.shutter_release()
            self.remaining_shots -= 1
            self.shots_taken += 1
            self.sleep_til_next()

    def sleep_til_next(self):
        next_time = self.first_time + (self.interval * self.shots_taken)
        sleep_time = next_time - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)

    def shutter_release(self):
        print("click {:.9}".format(time.perf_counter()))


class PiShutterServer(Flask):

    def __init__(self, *args, **kwargs):
        super(PiShutterServer, self).__init__(*args, **kwargs)

        self.shutter_thread = None


app = PiShutterServer(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/shutter/")
def add_something():
    if (not app.shutter_thread) or (not app.shutter_thread.is_alive()):
        app.shutter_thread = Shutter(10, 13)
        app.shutter_thread.start()

    return """
    <html><head>    <link rel="stylesheet" href="../static/style.css"></head><body>
    {} of {} every {} seconds
</body>
</html>
""".format(app.shutter_thread.remaining_shots, app.shutter_thread.total_shots,
           app.shutter_thread.interval)
