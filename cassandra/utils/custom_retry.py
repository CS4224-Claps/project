from cassandra import WriteType
from cassandra.cluster import RetryPolicy


class CustomRetry(RetryPolicy):
    def __init__(
        self, read_attempts: int, write_attempts: int, unavailable_attempts: int
    ):
        super()

    def on_read_timeout(
        self,
        query,
        consistency,
        required_responses,
        received_responses,
        data_retrieved,
        retry_num,
    ):
        if received_responses:
            return RetryPolicy.RETHROW
        elif retry_num < self.read_attempts:
            if required_responses / 2 > received_responses:
                return RetryPolicy.RETRY_NEXT_HOST
            return RetryPolicy.RETRY
        return RetryPolicy.RETHROW

    def on_write_timeout(
        self,
        query,
        consistency,
        write_type,
        required_responses,
        received_responses,
        retry_num,
    ):
        if write_type != WriteType.BATCH_LOG:
            return RetryPolicy.RETHROW

        if received_responses:
            return RetryPolicy.RETHROW
        elif retry_num < self.write_attempts:
            if required_responses / 2 > received_responses:
                return RetryPolicy.RETRY_NEXT_HOST
            return RetryPolicy.RETRY
        return RetryPolicy.RETHROW

    def on_unavailable(
        self, query, consistency, required_replicas, alive_replicas, retry_num
    ):
        if retry_num < self.unavailable_attempts:
            return RetryPolicy.RETRY
        return RetryPolicy.RETHROW
