from robointerface import *
from time import sleep
import sys
import threading
from util import *


# pinout
# M1: rotate
MOTOR_ROTATE = 1
# M2: pitch
MOTOR_PITCH = 2
# I1: pitch counter
I_PITCH_COUNTER = 1
# I2: button
I_BUTTON = 2
# I3: pitch boundary
I_PITCH_BOUNDARY = 3
# I4: rotate boundary
I_ROTATE_BOUNDARY = 4
# I5: ticker for rotation movement
I_ROTATE_TICKER = 5


def test_full_pitch(ri):
    # l -> away from motor
    # r -> towards motor

    #assert not ri.Digital(I_PITCH_BOUNDARY)
    ri.SetMotor(MOTOR_PITCH, 'l')
    wait_rise(ri, I_PITCH_BOUNDARY)
    ri.SetMotor(MOTOR_PITCH, 'r')
    wait_falling(ri, I_PITCH_BOUNDARY)
    wait_rise(ri, I_PITCH_BOUNDARY)
    ri.SetMotor(MOTOR_PITCH, 's')


def test_full_rotation_rl(ri):
    #assert not ri.Digital(I_ROTATE_BOUNDARY)
    ri.SetMotor(MOTOR_ROTATE, 'r', 7)
    wait_rise(ri, I_ROTATE_BOUNDARY)
    ri.SetMotor(MOTOR_ROTATE, 'l', 7)
    wait_falling(ri, I_ROTATE_BOUNDARY)
    wait_rise(ri, I_ROTATE_BOUNDARY)
    ri.SetMotor(MOTOR_ROTATE, 's')


def test_counter(ri, COUNTER):
    count = 0
    while True:
        current = ri.Digital(COUNTER)
        while current == ri.Digital(COUNTER):
            sleep(0.001)
        count += 1
        print(count)


def test_pitch_and_counter(ri):
    counter = threading.Thread(target=test_counter, args=(ri, I_PITCH_COUNTER), daemon=True)
    counter.start()
    test_full_pitch(ri)


def test_rotate_and_counter(ri):
    counter = threading.Thread(target=test_counter, args=(ri, I_ROTATE_TICKER), daemon=True)
    counter.start()
    test_full_rotation_rl(ri)


def motor_ticks(ri, conf, dir, ticks):
    ri.SetMotor(conf[0], dir)
    count = 0
    while True:
        current = ri.Digital(conf[1])
        while current == ri.Digital(conf[1]):
            sleep(0.001)
        count += 1
        if count == ticks:
            break
    ri.SetMotor(conf[0], 's')


if __name__ == '__main__':
    ri = RoboInterface()
    if not ri.hasInterface():
        print("could not find robo interface")
        sys.exit(-1)
    # test_full_rotation_rl(ri)
    # test_full_pitch(ri)
    # test_pitch_and_counter(ri)
    #test_rotate_and_counter(ri)

    motor_ticks(ri, (MOTOR_PITCH, I_PITCH_COUNTER), 'l', 9)


    ri.close()