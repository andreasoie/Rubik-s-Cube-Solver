#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author        : Andreas Øie


from sys import exit as Die

class Normalizer:

    def algorithm(self, alg):
        solution = []
        for notation in alg.split(' '):
            solution.append([notation])
        return solution

normalize = Normalizer()
