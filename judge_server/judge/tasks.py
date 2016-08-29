from __future__ import absolute_import

from celery import shared_task

from json import dumps

from problem.tasks import send_code_insert


@shared_task
def update_machine_data(machine_name):
    from .models import Machine
    from problem.models import MetaProblem, SpecialJudge
    from problem.documents import SpecialJudge as SpecialJudgeMongo

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

        meta_problem = MetaProblem.objects.get(id=mid)
        problems = meta_problem.problem.all()
        for problem in problems:
            if SpecialJudge.objects.filter(problem=problem).exists():
                special_judge = problem.special_judge
                eid = special_judge.environment
                pid = special_judge.problem_id

                send_code_insert(mid, str(pid), str(eid), str(SpecialJudgeMongo.get_code(str(pid))))
    return mids
