#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : video.py
# Author        : Kim K
# Created       : Fri, 29 Jan 2016
# Last Modified : Sun, 31 Jan 2016

from sys import exit as Die
import sys
import cv2
from colordetection import ColorDetector
import time

class WebCam:

    def __init__(self):
        self.cam              = cv2.VideoCapture(0)
        self.stickers         = self.get_sticker_coordinates('main')
        self.current_stickers = self.get_sticker_coordinates('current')
        self.preview_stickers = self.get_sticker_coordinates('preview')
        self.sides   = {}
        self.preview = ['white','white','white','white','white','white','white','white','white']
        self.state   = [0,0,0,0,0,0,0,0,0]

    def get_frame(self):
        _, frame = self.cam.read()
        return frame

    def test_method(self, yo, ya):
        """
        
        :param yo:
        :param ya:
        :return:
        """
        x = 5
        return x

    def get_sides(self):
        return self.sides

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
        print("Releasing camera")
        print("Destroying window")
        
    # param: coil_value
    def scan(self, frame, debug, take_picture):
        """
        Open up the webcam and scans the 9 regions in the center
        and show a preview in the left upper corner.

        After hitting the space bar to confirm, the block below the
        current stickers shows the current state that you have.
        This is show every user can see what the computer toke as input.

        :returns: dictionary
        """
        for x in range(5):
            if debug:
                #init certain stickers.
                self.draw_main_stickers(frame)
                self.draw_preview_stickers(frame, self.preview)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            for index,(x,y) in enumerate(self.stickers):
                roi          = hsv[y:y+32, x:x+32]
                avg_hsv      = ColorDetector.average_hsv(roi)
                color_name   = ColorDetector.get_color_name(avg_hsv)
                self.state[index] = color_name

            if take_picture == 1:
                self.preview = list(self.state)
                if debug:
                    self.draw_preview_stickers(frame, self.state)
                face = self.color_to_notation(self.state[4])
                notation = [self.color_to_notation(color) for color in self.state]
                self.sides[face] = notation
                
                # Face = the middle color
                # Places the list of colors on the correct side given by the face(what side it is)            
                # State = array of 9 colors representing the side
                # State: ['blue', 'blue', 'green', 'white', 'blue', 'white', 'orange', 'orange', 'green']
                # Notation = array of 9 letters represetning the color
                # Notation: ['B', 'B', 'D', 'U', 'B', 'U', 'L', 'L', 'F']
                # Face = a string of 1 letter representing the side. ex. B = blue
            if debug:
                self.draw_current_stickers(frame, self.state)
                text = 'scanned sides: {}/6'.format(len(self.sides))
                cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                cv2.imshow("Rubik's Cube camera", frame)
                


if __name__ == "__main__":

    cap = WebCam()

    while True:
        frame = cap.get_frame()
        cap.scan(frame, True, 1)
        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            cap.shutdown_camera()
            break

        
    
