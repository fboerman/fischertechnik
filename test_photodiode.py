from robointerface import *
import sys
from util import *
import json


# pinout
I_BUTTON = 2
O_LAMP = 5

NUM_SENSORS = 3
NUM_TESTS = 10

if __name__ == '__main__':
    ri = RoboInterface()
    if not ri.hasInterface():
        print("could not find robo interface")
        sys.exit(-1)
    data = []
    for n_s in range(NUM_SENSORS):
        print(f"waiting for sensor test {n_s} to start")
        data_sensor = []
        wait_rise(ri, I_BUTTON)
        for n in range(NUM_TESTS):
            print(f"run test {n}")
            data_row = []
            for i in reversed(range(8)):
                print(f"run intensity {i}")
                ri.SetOutput(O_LAMP, i)
                sleep(1)
                data_row.append(ri.GetAX())
                print(f"sensor reported {data_row[-1]}")
            data_sensor.append(data_row)
        data.append(data_sensor)

    with open('photonics_sensors_3dist_newsensor.json', 'w') as stream:
        json.dump(data, stream)
    print("done")
    print(json.dumps(data))