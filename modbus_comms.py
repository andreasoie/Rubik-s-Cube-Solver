#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusTcpClient



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

    
    def send_int(self, your_address, your_value):
        """
        Helper method for sending over rubiks-move-commands, sending 
        each move as a parsed String to represent a integer
        Check command_tables in folder for further information
        """
        reponse = self.client.write_register(your_address, your_value, unit=1)
        return reponse

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
        self.client.write_coils(0, 0)
        
    def set_confirm_picture_taken(self):
        """
        Confirm that we've taken a picture to the coil at the given address
        Usually read at the other end
        """
        self.client.write_coil(1, 1, unit=1)
        #picture_taken = coil_info.bits[1]
        #return picture_taken


if __name__ == "__main__":

    client = ModbusClient("158.38.140.61", port=2000)
    
    while client.is_connected:
        
        cam_command = client.get_picture_command()
        if cam_command:
            """
            preview = list(state)
            self.draw_preview_stickers(frame, state)
            face = self.color_to_notation(state[4])
            notation = [self.color_to_notation(color) for color in state]
            sides[face] = notation
            print("sides: " + str(len(sides)))
            """
            client.reset_picture_command()

        # Continue with our other shit

        


    