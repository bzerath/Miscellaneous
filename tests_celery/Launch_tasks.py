import tasks
import time
from pprint import pprint


if __name__ == "__main__":
    length = 5
    args = list(range(length))
    results = {}
    for i in range(length):
        results[i] = tasks.add.delay(i, i)
    while not all(ready := [r.ready() for r in results.values()]):
        print("Waiting", ready)
        time.sleep(0.5)
    results = {key: value.get() for key, value in results.items()}
    pprint(results)

    res = tasks.fetchall_query.delay(db_creds={"host": "localhost",
                                               "port": "5433",
                                               "dbname": "world_ic_night_2306",
                                               "user": "redpig",
                                               "password": "Flostib4"},
                                     query="SELECT COUNT(*) FROM working_mnr.route;")
    pprint(res.get())
