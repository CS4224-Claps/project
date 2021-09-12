import time

from psycopg2.extras import LoggingConnection, LoggingCursor
                                                               
class TimeLoggingCursor(LoggingCursor):
    def execute(self, query, vars=None):
        self.timestamp = time.time()
        return super(TimeLoggingCursor, self).execute(query, vars)

class TimeLoggingConnection(LoggingConnection):
    def filter(self, msg, curs):
        return " {} ms taken".format(int((time.time() - curs.timestamp) * 1000))

    def cursor(self, *args, **kwargs):
        kwargs.setdefault('cursor_factory', TimeLoggingCursor)
        return LoggingConnection.cursor(self, *args, **kwargs)
 
