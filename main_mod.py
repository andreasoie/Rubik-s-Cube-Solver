#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Kim K
# Created       : Tue, 26 Jan 2016
# Last edited by: Andreas Ø.

from sys import exit as Die
import kociemba
from combiner import combine
from video_mod import WebCam
from modbus_comms import ModbusClient
import cv2


# For debug / user-experience
#show = True

if __name__ == '__main__':

    client = ModbusClient("158.38.140.61", port=502)

    cam_cap = cv2.VideoCapture(0)
    camera = WebCam(cam_cap)

    key = cv2.waitKey(5) & 0xFF

    while client.is_connected():

        # Read command-address
        feedback = client.get_picture_command()
        
        camera.scan(feedback)

        # read scan-command from address
        if feedback:
            # client.update_color_addresses() Send 54 values to addresses
            client.set_confirm_picture_taken()
            client.reset_picture_command()

        color_state = camera.get_sides()
        client.update_color_state(color_state)
        
        if len(camera.get_sides()) == 6:
            camera.shutdown_camera()
            cube_state = camera.get_sides()
            unsolved_state = combine.sides(cube_state)
            algo = kociemba.solve(unsolved_state)
            print("Sending: " + algo)
            client.send_algorithm(algo)
            break

        if key == 27:
            camera.shutdown_camera()
            break
        
        
