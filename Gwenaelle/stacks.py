"""
Queue :      X  -> [XXXXXXX] -> X
Stack :      X <-> [XXXXXXX]
"""

##########
# STACKS #
##########

#
# def create_stack():
#     return []
#
#
# def is_empty(s):
#     return s == []
#
#
# def peek(s):
#     """ Return the first item of a stack """
#     if is_empty(s):
#         print("Error, the queue is empty.")
#     else:
#         return s[0]
#
#
# def s_push(s, x):
#     """ add an element to the stack """
#     if is_empty(s):
#         s.append(x)
#     else:
#         s = [x] + s
#     return s
#
#
# def s_pop(s):
#     """ remove an element of the stack
#             --> remove THE FIRST ELEMENT of the stack """
#     s.pop(0)
#     return s


def create_stack():
    return []


def is_empty(s):
    compteur = 0
    for item in s:
        compteur += 1
    if compteur == 0:
        return True
    else:
        return False


def peek(s):
    """ Return the first item of a stack """
    if is_empty(s):
        print("error")
    else:
        return s[0]


def s_push(s, x):
    """ add an element to the stack """
    return [x] + s


def s_pop(s):
    """ remove an element of the stack
            --> remove THE FIRST ELEMENT of the stack """
    new_stack = []
    compteur = 0
    for item in s:
        if compteur == 0:
            pass
        else:
            new_stack = new_stack + [item]
        compteur += 1
    return new_stack
