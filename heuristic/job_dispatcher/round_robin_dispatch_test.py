import datetime
import uuid

from unittest import TestCase
import round_robin_dispatch


class TestJobStrategy(TestCase):

    def test_round_robin_dispatch_case1(self):
        workers = [
            {"worker_id": "1", "jobs": [{}, {}, {}, {}]},
            {"worker_id": "2", "jobs": [{}]},
            {"worker_id": "3", "jobs": []},
        ]
        jobs = [{}, {}, {}]

        res = round_robin_dispatch.round_robin_dispatch(workers, jobs)
        self.assertEqual(0, len(res["1"]))
        self.assertEqual(1, len(res["2"]))
        self.assertEqual(2, len(res["3"]))


