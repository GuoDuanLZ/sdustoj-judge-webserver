from __future__ import absolute_import

from celery import shared_task

from json import dumps


@shared_task
def update_machine_data(machine_name):
    from .models import Machine

    machine = Machine.objects.filter(name=machine_name).first()
    mids = set()

    for environment in machine.environment.all():
        for limit in environment.limit.all():
            mid = limit.problem.meta_problem_id
            mids.add(mid)

    mids = list(mids)

    import redis
    from judge_server.redis_connections import pool

    r = redis.Redis(connection_pool=pool)
    for mid in mids:
        info = dumps({
            'isFiles': 'false',
            't': {
                'id': '--',
                'opt': 'insert',
                'mid': str(mid),
                'tid': '*'
            }
        })
        r.rpush(machine.data_queue, info)

    return mids
