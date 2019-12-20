#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author        : Andreas Øie

from pymodbus.client.sync import ModbusTcpClient
import time


class ModbusClient():

    """
    This class is tailored to represent a Client talking with a PLC-server,
    communicating by reading / writing values to given addresses
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.client = ModbusTcpClient(address, port)
        self.connection_status = self.client.connect()

    def is_connected(self):
        """
        :return: True if connection is active, False otherwise
        """
        return self.connection_status

    def stop_running(self):
        self.client.write_coil(3, 0, unit=1)

    def get_running_status(self):
        """
        Method for reading the progress-status 
        """
        coil_status = self.client.read_coils(3, 1, unit=1)
        run = coil_status.bits[0]
        return run
    
    def send_move(self, your_address, your_value):
        """
        Helper method for sending over rubiks-move-commands, sending 
        each move as a parsed String to represent a color-code
        Check command_tables in folder for further information
        """
        self.client.write_register(your_address, your_value, unit=1)

    def get_address_side(self, side):
        """
        Helper method for addressing correct side-code
        as a key for retrieving the correct values (starting address),
        for each spesific side 
        :param: 
        :returns: the 
        """
        address_side = { 0: 30, 1 : 39, 2 : 48, 3 : 57, 4 : 66, 5 : 75}
        return address_side[side]

    def update_color_state(self, side, color_state):
        """
        Method for updating the color-addresses
        with the correctly applied color-code
        """
        # starting address depending on the given side
        start_address = self.get_address_side(side)

        for notation in color_state:
            color_code = self.get_notation_to_code(notation)
            self.send_color_code(start_address, color_code)
            start_address += 1

    def send_color_code(self, addr, val):
        """
        Helper method sending the code to given address
        :param addr: the address to write
        :param val: the value to send
        """
        self.client.write_register(addr, val, unit=1)

    def get_picture_command(self):
        """
        Check if we're commaneded to take a picture. The coil we're subscribing to is usually
        controlled on the other end. We need to change this to False when we're taken the picture
        :return: true / false 
        """
        coil_info = self.client.read_coils(0, 1, unit=1)
        is_picture_ready = coil_info.bits[0]
        return is_picture_ready

    def reset_picture_command(self):
        """
        Reset the picture-command
        """
        #print("Resetting START")
        self.client.write_coil(0, 0, unit=1)
        #print("Resetting STOP ")
        
    def set_confirm_picture_taken(self):
        """
        Confirm that we've taken a picture to the coil at the given address
        (Usually read at the other end)
        """
        self.client.write_coil(1, 1, unit=1)

    def get_return_code(self, value):
        """
        Helper method to convert movement-command to movement-code
        :param: the notation to check
        :return: the movement-code
        """
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
        """ Helper method for converting notation to correct side-color
        :param: the notation to check
        :return: the color code
        """
        if notation == "U": return 0   # white
        elif notation == "F": return 5 # green
        elif notation == "L": return 3 # red
        elif notation == "B": return 1 # blue
        elif notation == "R": return 2 # orange
        elif notation == "D": return 4 # yellow

    def send_algorithm(self, answer):
        """
        Method for sending the required
        movements for solving the cube,
        one move for each address
        :param: a rubiks-cube-string 
        """
        # starting_address is 0
        data = answer.split(" ")
        for x in range(len(data)):
            val = int(self.get_return_code(data[x]))
            self.send_move(x, val)


""" For testing purposes """
if __name__ == "__main__":

    client = ModbusClient("10.22.177.89", port=502)
    
    while client.is_connected:

        # delay
        time.sleep(0.5)
        
        x = client.get_picture_command()
        print("Coil: " + str(x))

        # reset
        client.reset_picture_command()



        


    
