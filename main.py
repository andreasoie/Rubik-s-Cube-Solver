#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last edited by: Andreas Ø.

from sys import exit as Die
import kociemba
from combiner import combine
from video import WebCam
from modbus_comms import ModbusClient
import threading
import queue
import cv2


# For debug / user-experience
show = True

if __name__ == '__main__':

    #client = ModbusClient("158.38.140.61", port=2000)
    camera = WebCam()
    
    
    trigger = 0
    side_count = 0
    
    while True:
        
        frame = camera.get_frame()

        # total sides scanned
        #side_count = len(camera.get_sides())
        #print("Total sides: " + str(side_count))
        
        #if side_count == 6:
        #    camera.shutdown_camera()
        #    cube_state = camera.get_sides()
        #    unsolved_state = combine.sides(cube_state)
        #    algorithm = kociemba.solve(unsolved_state)
        #    print("Answer: " + algorithm)
        #    break
        
        camera.scan(frame, show, trigger)
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            camera.shutdown_camera()
            break

        #trigger = int(input("Enter: "))
        
        #if trigger == 1:
        #        camera.scan(frame, show, trigger)
        #        trigger = 0

        #print("Lap completed.")
        
        """
        total_sides = len(camera.get_sides())
        
        if total_sides == 6:

            unsolved_state = camera.get_sides()
            algorithm = kociemba.solve(unsolved_state)
            print("Answer: " + algorithm)
            # Send the answer ( algorithm ) to the server 
            break

        else:

            trigger = client.get_picture_command()

            if trigger:
                camera.scan():
                total_sides += 1
                client.reset_picture_command()
        """

                    
            
