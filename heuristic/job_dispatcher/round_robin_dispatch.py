

# round-robin 策略简单实现
# 按照worker的job的数量，以此
def round_robin_dispatch(workers, jobs, result=None):

    if result is None:
        result = {}

    if len(workers) == 0:
        return result

    for job in jobs:
        min_worker_id = None
        min_weight = 0
        for worker_info in workers:
            worker_id = worker_info['worker_id']
            if worker_id not in result:
                result[worker_id] = []

            worker_weight = len(worker_info['jobs']) + len(result[worker_id])
            if min_worker_id is None or worker_weight < min_weight:
                min_worker_id = worker_id
                min_weight = worker_weight

        result[min_worker_id].append(job)

    return result

