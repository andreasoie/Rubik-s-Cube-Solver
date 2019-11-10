#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Andreas Øie

from sys import exit as Die
import kociemba
from combiner import Combine
from video_mod import WebCam
from modbus_comms import ModbusClient
import cv2


# For debug / user-experience
#show = True

if __name__ == '__main__':

    client = ModbusClient("158.38.140.61", port=502)
    combine = Combine()

    cam_cap = cv2.VideoCapture(0)
    camera = WebCam(cam_cap)

    key = cv2.waitKey(5) & 0xFF

    count = 0

    while client.is_connected():

        running = client.get_running_status()

        if running:

            cam_trigger = client.get_picture_command()
            camera.scan(cam_trigger)

            if cam_trigger:
                color_state = camera.get_side(count)
                client.update_color_state(count, color_state)
                client.reset_picture_command()
                client.set_confirm_picture_taken()
                count += 1
            
            if len(camera.get_sides()) == 6:
                camera.shutdown_camera()
                cube_state = camera.get_sides()
                unsolved_state = combine.sides(cube_state)
                try: 
                    algo = kociemba.solve(unsolved_state)
                except ValueError:
                    client.stop_running()
                
                if running:
                    print("Sending: " + algo)
                    client.send_algorithm(algo)
                    break

            if key == 27:
                camera.shutdown_camera()
                break
        
        
