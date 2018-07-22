import threading
from threading import Thread
import time

from flask import Flask

try:
    import RPi.GPIO as GPIO
except ImportError:
    import mock_gpio as GPIO


class Shutter(Thread):

    def __init__(self, interval, total_shots, shutter_duration=0.1, focus_time=0, focus_port=18, shutter_port=16, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.shutter_duration = shutter_duration
        self.focus_time = focus_time
        if (interval > 5 and focus_time < 2):
            # after around 7 seconds the camera goes to sleep. we need a "focus" trigger to wake it up. we will just use 2 seconds for that
            self.focusTime = 2
        self.total_shots = total_shots
        self.remaining_shots = total_shots
        self.shots_taken = 0

        self.stop_condition = threading.Condition()

        self.focusPort = focus_port
        self.shutterPort = shutter_port

    def sleep_til_next(self):
        next_time = self.first_time + (self.interval * self.shots_taken)
        sleep_time = next_time - time.perf_counter()
        if sleep_time > 0:
            self.stop_condition.wait(sleep_time)

    def shutter_release(self):
        print("focus")
        GPIO.output(self.focusPort, True)
        if (self.focusTime > 0):
            time.sleep(self.focusTime)
        print("shutter")
        GPIO.output(self.shutterPort, True)

        time.sleep(self.shutter_duration)

        print("release")
        GPIO.output(self.shutterPort, False)
        GPIO.output(self.focusPort, False)

    def init_gpio(self):

        # Set the Board Mode
        GPIO.setmode(GPIO.BOARD)

        # Sets up GPIO Pin 11 to Output
        GPIO.setup(self.focusPort, GPIO.OUT)
        GPIO.setup(self.shutterPort, GPIO.OUT)

        GPIO.output(self.shutterPort, False)
        GPIO.output(self.focusPort, False)

    def cleanup(self):
        GPIO.output(self.focusPort, False)
        GPIO.output(self.shutterPort, False)

    def run(self):

        self.first_time = time.perf_counter()  # init based on perf_counter

        self.init_gpio()

        self.stop_condition.acquire()
        while self.remaining_shots > 0:
            self.shutter_release()
            self.remaining_shots -= 1
            self.shots_taken += 1
            self.sleep_til_next()


        print("done")
        self.stop_condition.release()
        self.cleanup()


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


@app.route("/stop/")
def stop():
    if app.shutter_thread and (app.shutter_thread.is_alive()):
        app.shutter_thread.remaining_shots = 0
        app.shutter_thread.stop_condition.acquire()
        app.shutter_thread.stop_condition.notify()
        app.shutter_thread.stop_condition.release()

    return """
    <html><head>    <link rel="stylesheet" href="../static/style.css"></head><body>
    stopped
</body>
</html>
"""
