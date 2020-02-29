"""
Queue :      X  -> [XXXXXXX] -> X
Stack :      X <-> [XXXXXXX]
"""

import Gwenaelle.stacks as stacks
import Gwenaelle.queues as queues


def exercice_1_1_v1_reverse(given_stack):
    output = stacks.create_stack()
    while not stacks.is_empty(given_stack):
        output = stacks.s_push(output, stacks.peek(given_stack))
        stacks.s_pop(given_stack)
    return output


def exercice_1_1_v2_reverse(given_stack):
    temp = queues.create_queue()
    output = stacks.create_stack()

    while not stacks.is_empty(given_stack):
        temp = queues.enqueue(temp, stacks.peek(given_stack))
        stacks.s_pop(given_stack)
    while not queues.is_empty(temp):
        output = stacks.s_push(output, queues.peek(temp))
        queues.de_queue(temp)
    return output


def exercice_1_2_count(given_stack):
    count = 0
    while not stacks.is_empty(given_stack):
        count += 1
        stacks.s_pop(given_stack)
    return count


def exercice_1_3_v1_add(given_stack, position, item):
    reversed_stack = exercice_1_1_v1_reverse(given_stack[:])
    length = exercice_1_2_count(given_stack)
    output = stacks.create_stack()
    cursor = 0
    while not stacks.is_empty(reversed_stack):
        if length-cursor == position:
            output = stacks.s_push(output, item)
        output = stacks.s_push(output, stacks.peek(reversed_stack))
        reversed_stack = stacks.s_pop(reversed_stack)
        cursor += 1
    return output


def exercice_1_3_v2_add(given_stack, position, item):
    temp_stack = stacks.create_stack()
    cursor = 0
    while cursor < position:
        temp_stack = stacks.s_push(temp_stack, stacks.peek(given_stack))
        given_stack = stacks.s_pop(given_stack)
        cursor += 1
    given_stack = stacks.s_push(given_stack, item)
    while not stacks.is_empty(temp_stack):
        given_stack = stacks.s_push(given_stack, stacks.peek(temp_stack))
        temp_stack = stacks.s_pop(temp_stack)
    return given_stack


def exercice_1_4a_remove(given_stack, to_remove):
    reversed_stack = exercice_1_1_v1_reverse(given_stack[:])
    output = stacks.create_stack()
    while not stacks.is_empty(reversed_stack):
        if stacks.peek(reversed_stack) != to_remove:
            output = stacks.s_push(output, stacks.peek(reversed_stack))
        reversed_stack = stacks.s_pop(reversed_stack)
    return output


def exercice_1_4b_remove(given_stack, to_remove):
    output = stacks.create_stack()
    removed = False
    while not stacks.is_empty(given_stack):
        if stacks.peek(given_stack) == to_remove and removed is not True:
            # add nothing
            removed = True
        else:
            output = stacks.s_push(output, stacks.peek(given_stack))
        given_stack = stacks.s_pop(given_stack)

    return exercice_1_1_v1_reverse(output[:])


def exercice_1_4c_remove(given_stack, number):
    output = stacks.create_stack()
    count = 0
    while not stacks.is_empty(given_stack):
        if count == number:
            pass
        else:
            output = stacks.s_push(output, stacks.peek(given_stack))
        count += 1
        given_stack = stacks.s_pop(given_stack)
    return exercice_1_1_v1_reverse(output)


def exercice_1_5():
    # Yes, by reversing one of the queues.
    pass


def exercice_2_1_reverse(given_queue):
    temp = stacks.create_stack()
    output = queues.create_queue()

    while not queues.is_empty(given_queue):
        temp = stacks.s_push(temp, queues.peek(given_queue))
        given_queue = queues.de_queue(given_queue)
    while not stacks.is_empty(temp):
        output = queues.enqueue(output, stacks.peek(temp))
        temp = stacks.s_pop(temp)
    return output


def exercice_2_2_count(given_queue):
    count = 0
    while not queues.is_empty(given_queue):
        count += 1
        queues.de_queue(given_queue)
    return count


def exercice_2_3_add(given_queue, position, item):
    output = queues.create_queue()
    length = exercice_2_2_count(given_queue[:])
    cursor = 0
    while not queues.is_empty(given_queue):
        if length-cursor == position:
            output = queues.enqueue(output, item)
        cursor += 1
        output = queues.enqueue(output, queues.peek(given_queue))
        given_queue = queues.de_queue(given_queue)
    return output


def exercice_2_4a_remove(given_queue, to_remove):
    output = queues.create_queue()
    while not queues.is_empty(given_queue):
        if queues.peek(given_queue) == to_remove:
            pass  # do nothing
        else:
            output = queues.enqueue(output, queues.peek(given_queue))
        queues.de_queue(given_queue)
    return output


def exercice_2_4b_remove(given_queue, to_remove):
    reversed_queue = exercice_2_1_reverse(given_queue[:])
    output = queues.create_queue()
    removed = False
    while not queues.is_empty(reversed_queue):
        if queues.peek(reversed_queue) == to_remove and removed is not True:
            removed = True
        else:
            output = queues.enqueue(output, queues.peek(reversed_queue))
        queues.de_queue(reversed_queue)
    return exercice_2_1_reverse(output[:])


def exercice_2_4c_remove(given_queue, number):
    output = queues.create_queue()
    length = exercice_2_2_count(given_queue[:])
    count = 0
    while not queues.is_empty(given_queue):
        if length-count-1 == number:
            pass
        else:
            output = queues.enqueue(output, queues.peek(given_queue))
        count += 1
        given_queue = queues.de_queue(given_queue)
    return output


if __name__ == "__main__":
    stack_exo_1_v1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    stack_exo_1_v2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("1.1 v1", exercice_1_1_v1_reverse(stack_exo_1_v1))
    print("1.1 v2", exercice_1_1_v2_reverse(stack_exo_1_v2))

    stack_exo_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("1.2", exercice_1_2_count(stack_exo_2))

    stack_exo_3_v1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    stack_exo_3_v2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("1.3 v1", exercice_1_3_v1_add(stack_exo_3_v1, position=3, item="a"))
    print("1.3 v2", exercice_1_3_v2_add(stack_exo_3_v2, position=3, item="a"))

    stack_exo4a = [0, 1, 2, 3, "a", 4, 5, 6, 7, "a", 8, "a", 9]
    print("1.4a", exercice_1_4a_remove(stack_exo4a, to_remove="a"))
    stack_exo4b = [0, 1, 2, 3, "a", 4, 5, 6, 7, "a", 8, "a", 9]
    print("1.4b", exercice_1_4b_remove(stack_exo4b, to_remove="a"))
    stack_exo4c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("1.4c", exercice_1_4c_remove(stack_exo4c, number=2))

    queue_exo_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("2.1", exercice_2_1_reverse(queue_exo_1))

    queue_exo_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("2.2", exercice_2_2_count(queue_exo_2))

    queue_exo_3 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("2.3", exercice_2_3_add(queue_exo_3, position=3, item="a"))

    queue_exo_4a = [0, 1, 2, 3, "a", 4, 5, 6, 7, "a", 8, "a", 9]
    print("2.4a", exercice_2_4a_remove(queue_exo_4a, to_remove="a"))
    queue_exo_4b = [0, 1, 2, 3, "a", 4, 5, 6, 7, "a", 8, "a", 9]
    print("2.4b", exercice_2_4b_remove(queue_exo_4b, to_remove="a"))
    queue_exo_4c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("2.4c", exercice_2_4c_remove(queue_exo_4c, number=2))

