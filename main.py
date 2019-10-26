#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last edited by: Andreas Ø.

from sys import exit as Die
import kociemba
from combiner import combine
from video import webcam
from modbus_comms import ModbusClient
import threading
import queue

not_testing = True

if __name__ == '__main__':

    client = ModbusClient("158.38.140.61", port=2000)

    # We run our image-analyzing in a thread, and update it through coil_que
    coil_queue = queue.Queue()
    threading.Thread(target= webcam.scan, args=(coil_queue,)).start()

    while client.is_connected:

        # Read only 1's (True values)
        coil_value = client.get_picture_command()
        coil_queue.put(coil_value)
        client.reset_picture_command()

        """
        # represents the state or a negative-scan (False)
        if not cube_state:
            print("Did not scan in all 6 sides.")
            Die(1)

        unsolvedState = combine.sides(cube_state)
        algorithm = kociemba.solve(unsolvedState)


        test_cube = "BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF"
        test_answer = kociemba.solve(test_cube)
        """