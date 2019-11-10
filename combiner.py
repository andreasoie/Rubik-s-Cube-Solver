#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Andreas Øie

class Combine:

    def __init__(self):
        pass

    def sides(self, sides):
        """Join all the sides together into one single string.

        :param sides: dictionary with all the sides
        :returns: string
        """
        combined = ''
        for face in 'URFDLB':
            combined += ''.join(sides[face])
        return combined

combine = Combine()