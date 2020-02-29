"""
Queue :      X  -> [XXXXXXX] -> X
Stack :      X <-> [XXXXXXX]
"""

import Gwenaelle.stacks as stacks
import Gwenaelle.queues as queues


def exercice_1_1_reverse(ma_stack):
    temp_queue = queues.create_queue()
    while not stacks.is_empty(ma_stack):
        temp_queue = queues.enqueue(temp_queue,
                                    stacks.peek(ma_stack))
        ma_stack = stacks.s_pop(ma_stack)
    while not queues.is_empty(temp_queue):
        ma_stack = stacks.s_push(ma_stack,
                                 queues.peek(temp_queue))
        temp_queue = queues.de_queue(temp_queue)
    return ma_stack


def exercice_1_2_count(ma_stack):
    compteur = 0
    while not stacks.is_empty(ma_stack):
        ma_stack = stacks.s_pop(ma_stack)
        compteur += 1
    return compteur


def exercice_1_3_add(ma_stack, position, item):
    pass
    # créer une stack temporaire avec les éléments de 0 à position-1
    temp_stack = stacks.create_stack()
    compteur = 0
    while compteur != position:
        temp_stack = stacks.s_push(temp_stack,
                                   stacks.peek(ma_stack))
        ma_stack = stacks.s_pop(ma_stack)
        compteur += 1
    # ajouter l'item dans ma_stack
    ma_stack = stacks.s_push(ma_stack,
                             item)
    # rapatrier la stack temporaire dans ma_stack
    while not stacks.is_empty(temp_stack):
        ma_stack = stacks.s_push(ma_stack,
                                 stacks.peek(temp_stack))
        temp_stack = stacks.s_pop(temp_stack)
    return ma_stack


def exercice_1_4a_remove(ma_stack, to_remove):
    temp_stack = stacks.create_stack()
    # On itère sur ma_stack, on insère chaque élément dans temp_stack SAUF s'il est == à to_remove
    while not stacks.is_empty(ma_stack):
        current_item_from_ma_stack = stacks.peek(ma_stack)
        if current_item_from_ma_stack == to_remove:
            pass
        else:
            temp_stack = stacks.s_push(temp_stack,
                                       current_item_from_ma_stack)
        ma_stack = stacks.s_pop(ma_stack)
    return exercice_1_1_reverse(temp_stack)


def exercice_1_4b_remove(ma_stack, to_remove):
    temp_stack = stacks.create_stack()
    found = False
    while not stacks.is_empty(ma_stack):
        current_item_from_ma_stack = stacks.peek(ma_stack)
        if found is False and current_item_from_ma_stack == to_remove:
            found = True
        else:
            temp_stack = stacks.s_push(temp_stack,
                                       current_item_from_ma_stack)
        ma_stack = stacks.s_pop(ma_stack)
    return exercice_1_1_reverse(temp_stack)


def exercice_1_4c_remove(ma_stack, number):
    temp_stack = stacks.create_stack()
    compteur = 0
    while not stacks.is_empty(ma_stack):
        if compteur != number:
            temp_stack = stacks.s_push(temp_stack,
                                       stacks.peek(ma_stack))
        else:
            pass
        ma_stack = stacks.s_pop(ma_stack)
        compteur += 1

    return exercice_1_1_reverse(temp_stack)


def exercice_1_5():
    """
    Oui, il faut créer une queue, l'inverser dans une seconde queue.
    t là, le premier entré sera le premier sorti.

    Exemple :

    queue1 = [0, 1, 2, 3, 4, 5, 6]
    C'est une queue, donc le dernier entré est 0, le premier qui sortira sera 6.
    queue2 = reverse(queue1) = [6, 5, 4, 3, 2, 1, 0]
    C'est une queue, donc le dernier entré est 6, le premier qui sortira sera 0.

    Chaîne = ( 0 --> [1, 2, 3, 4, 5, 6] -> reverse -> [6, 5, 4, 3, 2, 1] --> 0 )

    Ainsi, si on chaîne queue1 -> queue2, alors le dernier entré est 0, le premier qui sortira
    est 0.
    Ce qui équivaut à une stack.
    """




if __name__ == "__main__":
    stack_exo_1 = [0, 1, 2, 3, 4, 5, 6]
    print("1.1", exercice_1_1_reverse(stack_exo_1))

    stack_exo_2 = [0, 1, 2, 3, 4, 5, 6]
    print("1.2", exercice_1_2_count(stack_exo_2), stack_exo_2)

    stack_exo_3 = [0, 1, 2, 3, 4, 5, 6]
    print("1.3", exercice_1_3_add(stack_exo_3, position=3, item="a"))

    stack_exo4a = [0, 1, 2, "a", 3, 4, "a", 5, "a", 6]
    print("1.4a", exercice_1_4a_remove(stack_exo4a, to_remove="a"))
    stack_exo4b = [0, 1, 2, "a", 3, 4, "a", 5, "a", 6]
    print("1.4b", exercice_1_4b_remove(stack_exo4b, to_remove="a"))
    stack_exo4c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("1.4c", exercice_1_4c_remove(stack_exo4c, number=2))

    # queue_exo_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # print("2.1", exercice_2_1_reverse(queue_exo_1))
    #
    # queue_exo_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # print("2.2", exercice_2_2_count(queue_exo_2))
    #
    # queue_exo_3 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # print("2.3", exercice_2_3_add(queue_exo_3, position=3, item="a"))
    #
    # queue_exo_4a = [0, 1, 2, 3, "a", 4, 5, 6, 7, "a", 8, "a", 9]
    # print("2.4a", exercice_2_4a_remove(queue_exo_4a, to_remove="a"))
    # queue_exo_4b = [0, 1, 2, 3, "a", 4, 5, 6, 7, "a", 8, "a", 9]
    # print("2.4b", exercice_2_4b_remove(queue_exo_4b, to_remove="a"))
    # queue_exo_4c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # print("2.4c", exercice_2_4c_remove(queue_exo_4c, number=2))

