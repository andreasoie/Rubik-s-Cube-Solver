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
    client = ModbusClient("192.168.0.100", port=502)
    
    print("Connection: " + str(client.is_connected()))

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
                
                print("Taking picture")
                
                try:
                    client.set_confirm_picture_taken()
                    color_state = camera.get_side(pictures)
                    client.update_color_state(pictures, color_state)
                    client.reset_picture_command()
                    pictures += 1
                    print("Pictures: " + str(pictures))

                except KeyError:
                    print("Wrong notation color in the middle")
                    pictures = 0
                    camera.reset_sides()
                    client.stop_running()
                    camera.shutdown_camera_window()
                    
                    
            # If we're done taking pictures
            if pictures == 6:

                cube_state_sides = camera.get_sides()
                unsolved_state = combine.sides(cube_state_sides)
                
                algo = "error"
                
                try: 
                    algo = kociemba.solve(unsolved_state)
                    
                except ValueError:
                    pictures = 0
                    camera.reset_sides()
                    client.stop_running()
                    print("Error while solving. Resetting! ")
                    
                except TypeError:
                    pictures = 0
                    camera.reset_sides()
                    client.stop_running()
                    print("Error while solving. Resetting! ")
                
                if running:
                    
                    try:
                        print("--------------------------------")
                        print("Sending steps: " + algo)
                        print("--------------------------------")
                
                        client.send_algorithm(algo)
                        
                    except TypeError:
                        print("Non-valied cube state. Resetting! ")
                        pictures = 0
                        camera.reset_sides()
                        client.stop_running()
                        
                    finally:
                        pictures = 0
                        camera.reset_sides()
                        client.stop_running()
                        camera.shutdown_camera_window()
                        print("Ready for new scan .. ")

            # Incase of manual shutdown
            if key == 27:
                camera.shutdown_camera()
                break

        else:
            # Reset in case of STOP-button is pressed 
            pictures = 0
            camera.reset_sides()
        
        
