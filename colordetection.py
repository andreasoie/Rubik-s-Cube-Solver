#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Kim K
# Edited        : Andreas Øie
class ColorDetection:

    def get_color_name(self, hsv):
        """ Get the name of the color based on the hue.

        :returns: string
        """

        (h,s,v) = hsv

        if h > 120 and h < 195:
            return 'red'
        elif h > 7 and h < 20 and s > 170 and s < 250:
            return 'orange'
        elif h > 95 and h < 110 and s > 25 and s < 55:
            return 'white'
        elif h > 20 and h < 40 and s > 100 and s < 170:
            return 'yellow'
        elif h > 75 and h < 85:
            return 'green'
        elif h > 105 and h < 115 and s > 210 and s < 255:
            return 'blue'
        else:
            return 'white'

    def name_to_rgb(self, name):
        """
        Get the main RGB color for a name.

        :param name: the color name that is requested
        :returns: tuple
        """
        color = {
            'red'    : (0,0,255),
            'orange' : (0,165,255),
            'blue'   : (255,0,0),
            'green'  : (0,255,0),
            'white'  : (255,255,255),
            'yellow' : (0,255,255)
        }
        return color[name]

    def average_hsv(self, roi):
        """ Average the HSV colors in a region of interest.

        :param roi: the image array
        :returns: tuple
        """
        h   = 0
        s   = 0
        v   = 0
        num = 0
        for y in range(len(roi)):
            if y % 10 == 0:
                for x in range(len(roi[y])):
                    if x % 10 == 0:
                        chunk = roi[y][x]
                        num += 1
                        h += chunk[0]
                        s += chunk[1]
                        v += chunk[2]
        h /= num
        s /= num
        v /= num
        return (int(h), int(s), int(v))

ColorDetector = ColorDetection()
