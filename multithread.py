import collections
import datetime
import math
import pprint
import time
import multiprocessing
import multiprocessing.pool


def multithread_this_loop(func: collections.Callable,
                          iterable_to_loop_on: collections.Iterable):
    n_cpu = multiprocessing.cpu_count()
    with multiprocessing.pool.ThreadPool(n_cpu) as pool:
        instances = [pool.apply_async(func=func, args=[arg, i, "thread"])
                     for i, arg in enumerate(iterable_to_loop_on)]
        results = [instance.get() for instance in instances]

    return results


def multiproc_this_loop(func: collections.Callable,
                        iterable_to_loop_on: collections.Iterable):
    n_cpu = multiprocessing.cpu_count()
    with multiprocessing.Pool(n_cpu) as pool:
        instances = [pool.apply_async(func=func, args=[arg, i, "process"])
                     for i, arg in enumerate(iterable_to_loop_on)]
        results = [instance.get() for instance in instances]

    return results


def fonction(valeur, a, b):
    begin = time.time()
    valeur**(valeur-1)**(valeur-2)
    print(valeur, a, b)
    return {"i": a,
            "version": b,
            "current_time": datetime.datetime.now().strftime("""%H:%M'%S" """),
            "compute time": time.time()-begin}


if __name__ == "__main__":
    t = [9]*20
    print(t)
    begin = time.time()
    resultat_thread = multithread_this_loop(fonction,
                                            t)
    print("Multithread :", time.time() - begin)
    pprint.pprint(resultat_thread)

    begin = time.time()
    resultat_proc = multiproc_this_loop(fonction,
                                        t)
    print("Multiproc :", time.time() - begin)
    pprint.pprint(resultat_proc)

