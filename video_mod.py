#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Andreas Øie

from sys import exit as Die
import sys
import cv2
from colordetection import ColorDetector


class WebCam():

    """
    This class represents the state of the Rubik's Cube given
    by the scanned sides with the WebCam
    """
    
    def __init__(self, the_camera):
        self.cam              = the_camera
        self.stickers         = self.get_sticker_coordinates('main')
        self.current_stickers = self.get_sticker_coordinates('current')
        self.preview_stickers = self.get_sticker_coordinates('preview')
        self.sides   = {}
        self.preview = ['white','white','white','white','white','white','white','white','white']
        self.state   = [0,0,0,0,0,0,0,0,0]
        
    def get_sides(self):
        """
        Returns the state of the Cube
        """
        return self.sides
    
    def reset_sides(self):
        """
        Helper method for resetting the state of the Cube
        """
        self.sides   = {}
        self.preview = ['white','white','white','white','white','white','white','white','white']
        self.state   = [0,0,0,0,0,0,0,0,0]

    def get_side(self, numbr):
        """
        Returns a spesific side given by the number required
        :param numbr: the side number to retrieve
        """
        return self.sides[self.code_to_notation(numbr)]
        
    def code_to_notation(self, color):
        """
        Helper method for return the notation of the given color code
        :param color: the color (number) to retrieve
        """
        notation_colors = {
                0 : 'U',
                1 : 'F',
                2 : 'R',
                3 : 'B',
                4 : 'L',
                5 : 'D'
            }
        return notation_colors[color]

    def get_sticker_coordinates(self, name):
        """
        Every array has 2 values: x and y.
        Grouped per 3 since on the cam will be
        3 rows of 3 stickers.
        :param name: the requested color type
        :returns: list
        """
        stickers = {
            'main': [
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ]
        }
        return stickers[name]


    def draw_main_stickers(self, frame):
        """Draws the 9 stickers in the frame."""
        for x,y in self.stickers:
            cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)

    def draw_current_stickers(self, frame, state):
        """Draws the 9 current stickers in the frame."""
        for index,(x,y) in enumerate(self.current_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def draw_preview_stickers(self, frame, state):
        """Draws the 9 preview stickers in the frame."""
        for index,(x,y) in enumerate(self.preview_stickers):
            cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)

    def color_to_notation(self, color):
        """
        Return the notation from a specific color.
        We want a user to have green in front, white on top,
        which is the usual.
        :param color: the requested color
        """
        notation = {
            'green'  : 'F',
            'white'  : 'U',
            'blue'   : 'B',
            'red'    : 'R',
            'orange' : 'L',
            'yellow' : 'D'
        }
        return notation[color]

    def shutdown_camera(self):
        self.cam.release()
        cv2.destroyAllWindows()
        #print("Releasing camera")
        #print("Destroying window")
        
    def shutdown_camera_window(self):
        #print("Destroying window")
        cv2.destroyAllWindows()

    def scan(self, trigger):
        
        _, frame = self.cam.read()
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        key = cv2.waitKey(10) & 0xff
        
        self.draw_main_stickers(frame)
        self.draw_preview_stickers(frame, self.preview)

        for index,(x,y) in enumerate(self.stickers):
            roi          = hsv[y:y+32, x:x+32]
            avg_hsv      = ColorDetector.average_hsv(roi)
            color_name   = ColorDetector.get_color_name(avg_hsv)
            #print("Color: " + str(color_name) + ", avg_hsv  :  " + str(avg_hsv))
            self.state[index] = color_name

            # update when we recieve camera-command from input-param
            if trigger: 
                self.preview = list(self.state)
                self.draw_preview_stickers(frame, self.state)
                face = self.color_to_notation(self.state[4])
                notation = [self.color_to_notation(color) for color in self.state]
                self.sides[face] = notation
                #print(self.sides)

        # show the new stickers
        self.draw_current_stickers(frame, self.state)

        text = 'scanned sides: {}/6'.format(len(self.sides))
        cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        
        cv2.imshow("Rubiks", frame)


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    web = WebCam(cap)
    test_trigger = False

    while True:
        web.scan(test_trigger)
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            cap.shutdown_camera()
            break


    
