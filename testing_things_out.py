from modbus_comms import ModbusClient
from video_mod import WebCam
import cv2

def update_color_state(self, color_state):

    color_list = self.convert_sides_to_string(color_state)

    for lists in color_list:
        for color in lists:
            code = self.get_notation_to_code(color)
            self.send_color_code(address, code)
            address += 1

def get_address_side(side):
        # starting address for sending  colors
    address_side = { 1: 30, 2 : 39, 3 : 48, 4 : 57, 5 : 66, 6 : 75}
    return address_side[side]

def code_to_notation(color):
        notation_colors = {
                0 : 'U',
                1 : 'F',
                2 : 'L',
                3 : 'B',
                4 : 'R',
                5 : 'D'
            }
        return notation_colors[color]

def get_side(side_nr):
    cube_state = {
            "U": ['U','U','U','U','U','U','U','U','U'],
            "F": ['F','F','F','F','F','F','F','F','F'],
            "R": ['R','R','R','R','R','R','R','R','R'],
            "B": ['B','B','B','B','B','B','B','B','B'],
            "L": ['L','L','L','L','L','L','L','L','L'],
            "D": ['D','D','D','D','D','D','D','D','D']
            }
    dcube_state = {
            "U": ['U','U','U','U','U','U','U','U','U'],
            "F": ['U','U','U','U','U','U','U','U','U'],
            "R": ['U','U','U','U','U','U','U','U','U'],
            "B": ['U','U','U','U','U','U','U','U','U'],
            "L": ['U','U','U','U','U','U','U','U','U'],
            "D": ['U','U','U','U','U','U','U','U','U']
            }
    return cube_state[code_to_notation(side_nr)]

if __name__ == "__main__":
    
    client = ModbusClient("192.168.0.110", 502)

    if client.is_connected():

        print("Connected with 192.168.0.110")

        for x in range(6):
            side = get_side(x)
            client.update_color_state(x, side)

        print("Completed!")
