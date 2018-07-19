from threading import Thread
from time import sleep

from flask import Flask


class Shutter(Thread):

    def __init__(self, interval, total_shots, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.total_shots = total_shots
        self.remaining_shots = total_shots

    def run(self):
        while (self.remaining_shots > 0):
            sleep(self.interval)
            self.remaining_shots -= 1


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
        app.shutter_thread = Shutter(0.1, 100)
        app.shutter_thread.start()

    return """
    <html><head>    <link rel="stylesheet" href="../static/style.css"></head><body>
    {} of {} every {} seconds
</body>
</html>
""".format(app.shutter_thread.remaining_shots, app.shutter_thread.total_shots,
           app.shutter_thread.interval)
