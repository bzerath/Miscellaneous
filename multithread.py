import collections
import multiprocessing
from multiprocessing.pool import ThreadPool


def multithread_this_loop(func,
                          args: collections.Iterable):
    n_cpu = multiprocessing.cpu_count()
    pool = ThreadPool(n_cpu)
    results = []

    for arg in args:
        results.append(pool.apply_async(func=func,
                                        args=[arg]))

    pool.close()
    pool.join()

    return results



if __name__ == "__main__":
    print(type(multithread_this_loop))
