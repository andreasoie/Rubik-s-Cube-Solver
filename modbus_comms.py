#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusTcpClient
import time


class ModbusClient():

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.client = ModbusTcpClient(address, port)
        self.connection_status = self.client.connect()

    def is_connected(self):
        """
        :returns: True if connection is active, False otherwise
        """
        return self.connection_status

    
    def send_move(self, your_address, your_value):
        """
        Helper method for sending over rubiks-move-commands, sending 
        each move as a parsed String to represent a integer
        Check command_tables in folder for further information
        """
        self.client.write_register(your_address, your_value, unit=1)


    def convert_sides_to_string(self, sides):

        color_string = []
        
        for items in sides.values():
            color_string.append(items)

        return color_string

    def update_color_state(self, color_state):

        color_list = self.convert_sides_to_string(color_state)

        # starting address for sending  colors
        address = 30
        for lists in color_list:
            for color in lists:
                self.send_color_code(address, color)
                address += 1

    def send_color_code(self, addr, val):
        self.client.write_register(addr, val, unit=1)

    def read_int(self, your_address, your_value):
        """
        Reads a register address for checking value, this method is primarily used for
        error-checking or debugging without visual confirmation of the numbers in the
        given adresses
        """
        response = self.client.read_holding_registers(your_address, your_value, unit=1)
        return response

    def get_picture_command(self):
        """
        Check if we're commaneded to take a picture. The coil we're subscribing to is usually
        controlled on the other end. We need to change this to False when we're taken the picture
        """
        coil_info = self.client.read_coils(0, 1, unit=1)
        is_picture_ready = coil_info.bits[0]
        return is_picture_ready

        #TODO: Double check if this method works
    def reset_picture_command(self):
        """
        Set the take picture coil value to 0
        Is used after we've taken the picture
        """
        self.client.write_coil(0, 0, unit=1)
        
    def set_confirm_picture_taken(self):
        """
        Confirm that we've taken a picture to the coil at the given address
        Usually read at the other end
        """
        self.client.write_coil(1, 1, unit=1)
        #picture_taken = coil_info.bits[1]
        #return picture_taken

    # Helper method to convert notation to integers
    def get_return_code(self, value):
        if value == "B": return 1
        elif value == "U": return 2
        elif value == "L": return 3
        elif value == "D": return 4
        elif value == "R": return 5
        elif value == "F": return 6
        
        elif value == "B'": return 7
        elif value == "U'": return 8
        elif value == "L'": return 9
        elif value == "D'": return 10
        elif value == "R'": return 11
        elif value == "F'": return 12
        
        elif value == "B2": return 13
        elif value == "U2": return 14
        elif value == "L2": return 15
        elif value == "D2": return 16
        elif value == "R2": return 17
        elif value == "F2": return 18

    def get_notation_to_code(self, notation):
        if notation == "U": return 0   # white
        elif notation == "F": return 1 # green
        elif notation == "L": return 4 # red
        elif notation == "B": return 5 # blue
        elif notation == "R": return 3 # orange
        elif notation == "D": return 2 # yellow

    def send_algorithm(self, answer):
        data = answer.split(" ")
        for x in range(len(data)):
            val = int(self.get_return_code(data[x]))
            self.send_move(x, val)


if __name__ == "__main__":

    client = ModbusClient("10.22.177.89", port=502)
    
    while client.is_connected:

        # delay
        time.sleep(0.5)
        
        x = client.get_picture_command()
        print("Coil: " + str(x))

        # reset
        client.reset_picture_command()



        


    
