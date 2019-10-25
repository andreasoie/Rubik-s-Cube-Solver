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

not_testing = True

if __name__ == '__main__':

    client = ModbusClient("158.38.140.61", port=2000)

    # Maybe initialize inside while loop?
    cube_state = webcam.scan()

    while client.is_connected:

        status = client.get_picture_command()
        if status:

            #@TODO: FIX TAKE PICTURE FUNCTION
            #webcam.take_picture()
            client.reset_picture_command()

        # represents the state or a negative-scan (False)
        if not cube_state:
            print("Did not scan in all 6 sides.")
            Die(1)

        unsolvedState = combine.sides(cube_state)
        algorithm = kociemba.solve(unsolvedState)


        # test_cube = "BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF"
        # test_answer = kociemba.solve(test_cube)
