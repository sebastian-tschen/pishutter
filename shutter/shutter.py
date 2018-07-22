import threading
from threading import Thread
import time

from flask import Flask, render_template, request

try:
    import RPi.GPIO as GPIO
except ImportError:
    import mock_gpio as GPIO


class Shutter(Thread):

    def __init__(self, interval, total_frames, shutter_duration=0.1, focus_time=0, focus_port=18, shutter_port=16, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = float(interval)
        self.shutter_duration = float(shutter_duration)
        self.focus_time = float(focus_time)
        if (interval > 5 and focus_time < 2):
            # after around 7 seconds the camera goes to sleep. we need a "focus" trigger to wake it up. we will just use 2 seconds for that
            self.focusTime = 2
        self.total_shots = int(total_frames)
        self.remaining_shots = int(total_frames)
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


def process(*args):
    for string in args:
        if string == "oreos":
            return True

    return False


last_used_values = {
    "interval": 4,
    "total_frames": 30,
    "focus_time": 2,
    "shutter_duration": 0.1,
}

last_fps_values = {
    "fps": 30,
    "shoot_duration": 2,
    "clip_duration": 10,
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.form["submit"] == "submit":
        doritos = request.form["doritos"]
        oreos = request.form["oreos"]
        success = process(doritos, oreos)

        return render_template("index.html", fooResponse="Successful" if success else "Failed")

    elif request.form["submit"] == "pita":
        success = process("pita")
        return render_template("index.html", cooResponse="Successful" if success else "Failed")

    elif request.form["submit"] == "chip":
        success = process("chip")
        return render_template("index.html", cooResponse="Successful" if success else "Failed")


def is_running():
    return app.shutter_thread and (app.shutter_thread.is_alive())


@app.route("/fps", methods=["POST", "GET"])
def fps():
    if is_running():
        return render_template("is_running.html")

    if request.method == "GET":
        return render_template("fps.html", **last_fps_values)

    fps = float(request.form["fps"])
    shoot_duration = float(request.form["shoot_duration"])
    clip_duration = float(request.form["clip_duration"])
    total_frames = fps * clip_duration
    interval = (shoot_duration * 3600) / total_frames

    return render_template("shutter.html", interval=interval, total_frames=total_frames)


@app.route("/start", methods=["POST"])
def start():
    app.shutter_thread = Shutter(**(request.form))
    app.shutter_thread.start()


@app.route("/shutter", methods=["GET", "POST"])
def shutter():
    if is_running():
        return render_template("is_running.html")

    if request.method == "GET":
        return render_template("shutter.html", **last_used_values)
    if request.method == "POST":
        return render_template("shutter.html", **request.form)


@app.route("/stop", methods=["POST"])
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
