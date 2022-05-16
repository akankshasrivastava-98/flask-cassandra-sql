
import cassandra
import cassandra.pool
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.cqlengine import connection
from cassandra.cqlengine.connection import (cluster as cql_cluster, session as cql_session)
from cassandra.policies import RoundRobinPolicy, RetryPolicy, ExponentialReconnectionPolicy
from flask import current_app as app

try:
    from uwsgidecorators import postfork
except:
    def postfork(f):return f

_session_domestic = None

class ModifiedCassandraRetryPolicy(RetryPolicy):
    def on_read_timeout(self, query, consistency, required_responses,
                        received_responses, data_retrieved, retry_num):
        if retry_num != 0:
            return self.RETRY_NEXT_HOST, ConsistencyLevel.ONE
        elif received_responses >= required_responses and not data_retrieved:
            return self.RETRY_NEXT_HOST, ConsistencyLevel.ONE
        else:
            return self.RETRY_NEXT_HOST, ConsistencyLevel.ONE

@postfork
def cassandra_init():
    if cql_cluster is not None:
        cql_cluster.shutdown()
    if cql_session is not None:
        cql_session.shutdown()

    connection.setup(
        hosts=["0.0.0.0"],
        default_keyspace='test_keyspace', consistency=cassandra.ConsistencyLevel.ONE, lazy_connect=True, retry_connect=True,
        load_balancing_policy=RoundRobinPolicy(), compression=True,
        executor_threads=4,
        default_retry_policy=ModifiedCassandraRetryPolicy(),
        reconnection_policy=ExponentialReconnectionPolicy(base_delay=2, max_delay=10))


cassandra_init()


class CassandraManager(object):

    def _get_cassandra_session(self, keyspace_name="test_key2"):
        if keyspace_name == "test_key2":
            global _session_domestic
            if _session_domestic is not None:
                return _session_domestic
            else:

                cluster = Cluster(
                                  load_balancing_policy=RoundRobinPolicy(), compression=True, executor_threads=4,
                                  default_retry_policy=RetryPolicy.RETRY_NEXT_HOST,
                                  reconnection_policy=ExponentialReconnectionPolicy(base_delay=2, max_delay=10))
                _session_domestic = cluster.connect(keyspace=keyspace_name)

                return _session_domestic

    def get_user_details(self):
        try:
            query = "select * from emp_by_id where id=1 ;"
            session = self._get_cassandra_session()
            data= session.execute(query)
            return data
        except Exception as e:
            raise e
