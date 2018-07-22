class GPIO():
    pass


def output(focusPort, param):
    print("output: {} - {}".format(focusPort,param))


def setmode(BOARD):
    print("setmode: {}".format(BOARD))


def setup(focusPort, OUT):
    print("setup: {} - {}".format(focusPort, OUT))



BOARD="BOARD"
OUT="OUT"