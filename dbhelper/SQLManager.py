from mysql.connector import Error
from mysql.connector import pooling

connection_object = None

class MySQLManager(object):
    def _get_sql_session(self):

        global connection_object

        if connection_object is not None:
            if connection_object.is_connected():
                cursor = connection_object.cursor()
                return cursor 
        else:
            connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                pool_size=5,
                                                pool_reset_session=True,
                                                host='localhost',
                                                database='demo',
                                                user='root',
                                                password='Riksha@2803')
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor()
            return cursor

    def get_from_sqlDB(self):
        try:
            cursor = self._get_sql_session()
            cursor.execute("SELECT * FROM demo1;")
            data = cursor.fetchall()
            return data
        except Exception as e:
            raise e
