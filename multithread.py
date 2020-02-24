import collections
import multiprocessing
from multiprocessing.pool import ThreadPool


def multithread_this_loop(func: collections.Callable,
                          iterable_to_loop_on: collections.Iterable):
    n_cpu = multiprocessing.cpu_count()
    pool = ThreadPool(n_cpu)
    results = []

    for arg in iterable_to_loop_on:
        results.append(pool.apply_async(func=func,
                                        args=[arg]))

    pool.close()
    pool.join()

    return results
