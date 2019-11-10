#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Andreas Øie

from sys import exit as Die
import kociemba
from combiner import combine
from video_mod import WebCam
from modbus_comms import ModbusClient
import cv2


# For debug / user-experience
#show = True

if __name__ == '__main__':

    # IP of PLC-Server
    client = ModbusClient("158.38.140.61", port=502)

    cam_cap = cv2.VideoCapture(0)
    camera = WebCam(cam_cap)

    key = cv2.waitKey(5) & 0xFF

    pictures = 0

    while client.is_connected():

        running = client.get_running_status()

        if running:

            cam_trigger = client.get_picture_command()
            camera.scan(cam_trigger)

            if cam_trigger:
                color_state = camera.get_side(pictures)
                client.update_color_state(pictures, color_state)
                client.reset_picture_command()
                client.set_confirm_picture_taken()
                pictures += 1
            
            if pictures == 6:
                cube_state_sides = camera.get_sides()
                unsolved_state = combine.sides(cube_state_sides)
                try: 
                    algo = kociemba.solve(unsolved_state)
                except ValueError:
                    pictures = 0
                    client.stop_running()
                
                if running:
                    print("Sending steps: " + algo)
                    client.send_algorithm(algo)
                    break

            if key == 27:
                camera.shutdown_camera()
                break
        
        
