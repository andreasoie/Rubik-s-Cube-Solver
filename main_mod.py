#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Andreas Øie
# Created       : 09.11.2019

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

    count = 0

    while client.is_connected():

        # Camera-trigger
        cam_trigger = client.get_picture_command()

        camera.scan(cam_trigger)

        if cam_trigger:
            # client.update_color_addresses() Send 54 values to addresses
            color_state = camera.get_side(count)
            client.update_color_state(count, color_state)
            client.reset_picture_command()
            client.set_confirm_picture_taken()
            count += 1
        
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
        
        
