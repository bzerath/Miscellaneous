# queues functions
from typing import List, Any


def create_queue():
    return ([])


q = create_queue()


# same for stack
def is_empty(queue):
    return (queue == [])


# same for stack
def peek(queue):
    if is_empty(queue):
        print('error, the queue is empty')
    else:
        return(queue[0])


def enqueue(queue, x):
    queue.append(x)
    return(queue)


def de_queue(queue):
    queue.pop(0)
    return(queue)


# stacks functions
def create_stack():
    return ([])


def s_push(stack, x):
    if is_empty(stack):
        stack.append(x)
    else:
        stack = stack + [x]
    return stack


def s_stack(stack):
    stack.pop(0)
    return stack


# exercise 1
# question 1
def reverse(stack):
    queue = create_queue()
    # create a temporal queue
    while not is_empty(stack):
        # we check if the stack is empty each time
        queue = enqueue(queue, peek(stack))
        print(queue)
        # we add the last element of the stack and put in the queue
        stack = s_stack(stack)
        print(stack)
        # empty the stack
    while not is_empty(queue):
        # we check each time if the queue is empty
        stack = s_push(stack, peek(queue))
        # we add the first element of the queue in the stack
        queue = de_queue(queue)
        # empty the queue
    return stack  # optional


# question 2
def count_stack(stack):
    bis = create_stack()
    counter = 0
    # initialize the counter
    while not is_empty(stack):
        counter = +1
        # count each round
        stack = s_push(bis, peek(stack))
        s_stack(stack)
    while not is_empty(bis):
        stack = s_push(bis, peek(stack))
        s_stack(stack)
    return counter, stack


# question 3
def add(stack, x, p):
    # we create another stack to store the items
    stack1 = create_stack()
    # we count the item in the stack given b y the user
    lenghtstack = count_stack(stack)
    # we set 2 conditions for the loop statement
    # condition 1: while p > 1 we remove item
    # condition 2: if p is more than  the length of the given stack the loop will not be executed
    while (p > 1) and (p <= lenghtstack):
        # we take the item of stack and put them in stack1
        s_push(stack1, peek(stack))
        # we remove the moved items in stack
        s_stack(stack)
        # we decrease p
        p -= 1
    # put the item in s
    s_push(stack, x)
    # we check each time if the stack is empty
    while not is_empty(stack1):
        # we take the item of stack1 and put them in stack
        s_push(stack, peek(stack1))
        # we empty the temporal stack1
        s_stack(stack1)
    return stack


stack = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

j = reverse(stack)

print(j)

#question 4

def remove_all(stack, elt):
    stack1= create_stack()
    while not is_empty(stack):
        if peek(stack) != elt:
            stack = s_push(stack1, peek(stack))
        s_stack(stack)
    while not is_empty(stack1):
        stack= s_push(stack,peek(stack1))
        s_stack(stack1)

def remove_1St(stack, elt):
    stack1= create_stack()
    while not is_empty(stack):
        if peek(stack)== elt:
            s_stack(stack)
            break
        else:
            stack1= s_push(stack1,peek(stack))
    while not is_empty(stack1):
        stack= s_push(stack,peek(stack1))
        s_stack(stack1)
