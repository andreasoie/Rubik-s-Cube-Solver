#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename      : normalizer.py
# Author        : Kim K
# Created       : Sat, 30 Jan 2016
# Last Modified : Mon, 01 Feb 2016


from sys import exit as Die

class Normalizer:

    def algorithm(self, alg):
        solution = []
        for notation in alg.split(' '):
            solution.append([notation])
        return solution

normalize = Normalizer()
