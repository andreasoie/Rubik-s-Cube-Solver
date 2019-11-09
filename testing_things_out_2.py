
UPPER = (110, 55, 225)
LOWER = (95, 25, 185)

(h, s, v) = 100, 0, 0

if (h, s, v) > LOWER and (h, s, v) < UPPER:
    print(h, s, v)
    print("LW: " + str(LOWER))
    print("UP: " + str(UPPER))
else:
    print("nope")

