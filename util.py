from time import sleep


def wait_rise(ri, i):
    while ri.Digital(i):
        sleep(0.001)
    while not ri.Digital(i):
        sleep(0.001)


def wait_falling(ri, i):
    while ri.Digital(i):
        sleep(0.001)
    while ri.Digital(i):
        sleep(0.001)