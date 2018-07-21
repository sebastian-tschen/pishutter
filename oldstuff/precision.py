import random
import time


def check_time_precision():
    a = 20
    while a > 0:
        a -= 1
        time_to_sleep = (10 * random.random())
        oldtime = time.perf_counter()
        time.sleep(time_to_sleep)
        newtime = time.perf_counter()
        elapsed_time = newtime - oldtime
        diff = abs(elapsed_time - time_to_sleep)
        perc = (diff / time_to_sleep) * 100
        print("soll {:.4} | ist {:.4} - Abweichung {:.4}s, ({:.4}%)".format(time_to_sleep, elapsed_time, diff, perc))


check_time_precision()
