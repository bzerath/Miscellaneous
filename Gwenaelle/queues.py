"""
Queue :      X  -> [XXXXXXX] -> X
Stack :      X <-> [XXXXXXX]
"""

##########
# QUEUES #
##########


# def create_queue():
#     return []
#
#
# def is_empty(q):
#     return q == []
#
#
# # def peek(q):
# #     """ Return the first item of a Queue """
# #     if is_empty(q):
# #         print("Error, the queue is empty.")
# #     else:
# #         return q[0]
# def peek(q):
#     """ Return the first item of a Queue """
#     if is_empty(q):
#         print("Error, the queue is empty.")
#     else:
#         return q[-1]
#
#
# # def enqueue(q, x):
# #     """ Add an element to the queue """
# #     q.append(x)
# #     return q
# def enqueue(q, x):
#     """ Add an element to the queue """
#     q = [x] + q
#     return q
#
#
# # def de_queue(q):
# #     """ remove an element of the queue
# #         --> remove THE FIRST ELEMENT of the queue """
# #     q.pop(0)  #  list.pop([i]) =  Enlève de la liste l'élément situé à la position indiquée
# #     # et le renvoie en valeur de retour.
# #     return q
# def de_queue(q):
#     """ remove an element of the queue
#         --> remove THE FIRST ELEMENT of the queue """
#     q.pop(-1)  #  list.pop([i]) =  Enlève de la liste l'élément situé à la position indiquée
#     # et le renvoie en valeur de retour.
#     return q

def create_queue():
    return []


def is_empty(q):
    compteur = 0
    for item in q:
        compteur += 1
    if compteur == 0:
        return True
    else:
        return False


def peek(q):
    """ Return the first item of a Queue """
    return q[len(q)-1]  # equivalent: return q[-1]


def enqueue(q, x):
    """ Add an element to the queue """
    return [x] + q


def de_queue(q):
    """ remove an element of the queue
        --> remove THE LAST ELEMENT of the queue """
    new_queue = []
    compteur = 0
    len_of_q = len(q)
    for item in q:
        if compteur == len_of_q - 1:
            pass
        else:
            new_queue = new_queue + [item]
        compteur += 1
    return new_queue
