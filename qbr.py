#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last edited by: Andreas Ø.

from sys import exit as Die
import kociemba
from combiner import combine
from video import webcam


not_testing = True

if __name__ == '__main__':

    while True:

        if not_testing:

            # represents the state or a negative-scan (False)
            cube_state = webcam.scan()

            if not cube_state:
                print("Did not scan in all 6 sides.")
                Die(1)

            unsolvedState = combine.sides(cube_state)
            algorithm = kociemba.solve(unsolvedState)

        else:
            test_cube = "BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF"
            test_answer = kociemba.solve(test_cube)

            size_list = []
            words = test_answer.split(" ")
            for w in words:
                size_list.append(w)
            print("Solution:")
            print(test_answer)
            print("with: " + str(len(size_list)) + " moves")
            Die(1)
