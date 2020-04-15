def flag(T):
    i_blue = 0
    i_red = len(T)-1
    i_current = 0
    while i_current <= i_red:
        if T[i_current] == "White":
            i_current += 1
        elif T[i_current] == "Red":
            T[i_current], T[i_red] = T[i_red], T[i_current]
            i_red -= 1
        else:
            T[i_current], T[i_blue] = T[i_blue], T[i_current]
            if i_current == i_blue:
                i_current += 1
            i_blue += 1


T = ["White", "Blue", "Blue", "Red", "Blue", "White", "Blue"]
flag(T)
print(T)

T = ["Blue", "Red", "White", "Blue", "Blue", "Red", "White", "White", "Red", "Blue"]
flag(T)
print(T)
