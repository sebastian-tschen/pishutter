import logging

class GPIO():
    pass


def output(focusPort, param):
    logging.debug("output: {} - {}".format(focusPort,param))


def setmode(BOARD):
    logging.debug("setmode: {}".format(BOARD))


def setup(focusPort, OUT):
    logging.debug("setup: {} - {}".format(focusPort, OUT))



BOARD="BOARD"
OUT="OUT"