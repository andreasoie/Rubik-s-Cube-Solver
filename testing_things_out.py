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


notat = "F"
x = notation_to_values(notat)
print(x)