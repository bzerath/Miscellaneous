import collections.abc as collections
import datetime
import time
import multiprocessing
import multiprocessing.pool
import matplotlib
import matplotlib.pyplot as plt


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
    # print(valeur, a, b)
    (valeur**valeur**(valeur-2))#*(valeur**valeur**(valeur-2))*(valeur**valeur**(valeur-2))
    # (valeur**valeur**(valeur-2))*(valeur**valeur**(valeur-2))*(valeur**valeur**(valeur-2))
    # valeur**(valeur-1)**(valeur-2)
    return {"i": a,
            "version": b,
            "current_time": datetime.datetime.now().strftime("""%H:%M'%S" """),
            "compute time": time.time()-begin}


if __name__ == "__main__":
    main_value = 9
    length = 40

    estimations_sequentielles = []
    temps_multithreads = []
    temps_multiprocs = []

    for l in range(1, length+1):
        print("\n", l)
        t = [main_value] * l

        begin = time.time()
        fonction(main_value, -1, "solo")
        fonction(main_value, -1, "solo")
        fonction(main_value, -1, "solo")
        estimation_sequentiel = ((time.time() - begin)/3)*l
        print("Estimation en séquentiel :", estimation_sequentiel)
        estimations_sequentielles.append(round(estimation_sequentiel, 2))

        begin = time.time()
        resultat_thread = multithread_this_loop(fonction,
                                                t)
        temps_multithread = time.time() - begin
        print("Multithread :", temps_multithread)
        temps_multithreads.append(round(temps_multithread, 2))
        # pprint.pprint(resultat_thread)

        begin = time.time()
        resultat_proc = multiproc_this_loop(fonction,
                                            t)
        temps_multiproc = time.time() - begin
        print("Multiproc :", temps_multiproc)
        temps_multiprocs.append(round(temps_multiproc, 2))
        # pprint.pprint(resultat_proc)

        ratio = estimation_sequentiel/temps_multithread
        print("La version multi-thread est {} fois plus {} que la version séquentielle.".format(
            round(1 - ratio, 2) * -1 if ratio > 1 else round(1 - ratio, 2),
            "rapide" if ratio > 1 else "lente"
        ))
        ratio = temps_multithread/temps_multiproc
        print("La version multi-process est {} fois plus {} que la version multi-thread.".format(
            round(1 - ratio, 2) * -1 if ratio > 1 else round(1 - ratio, 2),
            "rapide" if ratio > 1 else "lente"
        ))

    print(estimations_sequentielles)
    print(temps_multithreads)
    print(temps_multiprocs)
    results = [round(1 - temps_multithread/temps_multiproc, 2) * -1
               for i, (temps_multithread,
                       temps_multiproc) in enumerate(zip(temps_multithreads,
                                                         temps_multiprocs))]
    for i, temps in enumerate(results):
        print(i+1, "\t", temps)

    fig, ax = plt.subplots()
    ax.plot(range(1, length+1),
            results)
    ax.set(xlabel="table length",
           ylabel="gain ratio")
    ax.grid()

    plt.xticks(range(0, length, 4))
    plt.show()


