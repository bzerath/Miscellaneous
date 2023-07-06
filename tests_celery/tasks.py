from celery import Celery
import psycopg2
import time
import logging

LOG = logging.getLogger(__name__)

app = Celery('tasks',
             backend='rpc://',
             broker='pyamqp://guest@localhost//')

DB_CONNECTION_TIMEOUT = 10


class DatabaseConnectionManager:
    """
    Context manager to get a database connection.
    Does not include any automatic commit.
    Isolation level = READ_COMMITTED
    """
    def __init__(self,
                 host: str,
                 port: str,
                 dbname: str,
                 user: str,
                 password: str,
                 schema: str = None,
                 connect_timeout: int = DB_CONNECTION_TIMEOUT):

        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.schema = schema
        self.db_creds = {"host": self.host,
                         "port": self.port,
                         "dbname": self.dbname,
                         "user": self.user,
                         "password": self.password,
                         "connect_timeout": connect_timeout}
        self.connection = None

    def __enter__(self) -> psycopg2.extensions.connection:
        """ Function called at the entrance of the 'with' statement. """
        self.connection = psycopg2.connect(**self.db_creds)
        LOG.debug("map_incident:connection_manager: Established connection "
                  "{_id} with {d}@{h}:{p} as user '{u}'.".format(
                      d=self.dbname,
                      h=self.host,
                      p=self.port,
                      u=self.user,
                      _id=id(self.connection)))
        self.connection.set_session(
            autocommit=True,
            isolation_level=psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Function called at the exit of the 'with' statement. """
        if self.connection is not None:
            LOG.debug("map_incident:connection_manager: Closing connection "
                      "{_id} with {d}@{h}:{p} as user '{u}'.".format(
                          d=self.dbname,
                          h=self.host,
                          p=self.port,
                          u=self.user,
                          _id=id(self.connection)))
            self.connection.close()


@app.task()
def add(x, y):
    time.sleep(1)
    return x + y


@app.task()
def fetchall_query(db_creds: dict, query: str):
    with DatabaseConnectionManager(**db_creds) as connection:
        with connection.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
    return results
