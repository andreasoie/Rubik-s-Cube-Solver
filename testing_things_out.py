def notation_to_values(notation):
        values = {
            'F' : 1,
            'U' : 2,
            'B' : 3,
            'R' : 4,
            'L' : 5,
            'D' : 6
        }
        return values[notation]

def convert_sides_to_string(sides):
    
    color_string = []

    for items in sides.values():
        color_string.append(items)

    #color_string = color_string.replace("'", "")
    return color_string

cube_state = {
  "U": ['F','R','R','U','B','U','D','L','R'],
  "F": ['x','x','x','x','x','x','x','x','x'],
  "R": ['x','x','x','x','x','x','x','x','x'],
  "B": ['x','x','x','x','x','x','x','x','x'],
  "L": ['x','x','x','x','x','x','x','x','x'],
  "D": ['x','x','x','x','x','x','x','x','x']
}

sss = convert_sides_to_string(cube_state)
print(str(sss))
temp = 0
for x in sss:
    for y in x:
        print(y)
        temp += 1

print(temp)
