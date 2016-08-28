from __future__ import absolute_import

from celery import shared_task

from json import dumps

# data##################################################################################################################


def _get_data_machines_to_inform(mid=None, tid=None, machine_name=None):
    from judge.models import Machine
    from .models import Environment, TestData
    if mid is None:
        if machine_name is None:
            machines = {machine.data_queue for machine in Machine.objects.all()}
        else:
            machine = Machine.objects.get(name=machine_name)
            machines = {machine.data_queue}
    else:
        envs = Environment.objects.filter(limit__problem__meta_problem_id=mid).distinct()
        machines = set()
        for env in envs:
            env_machines = env.machine.all()
            for machine in env_machines:
                machines.add(machine.data_queue)
    return machines


def _get_data_insert_info(mid=None, tid=None):
    info = {
        'isFiles': 'false',
        't': {
            'id': '--',
            'opt': 'insert',
            'mid': '*' if mid is None else str(mid),
            'tid': '*' if tid is None else [str(tid)]
        }
    }
    return info


def _get_data_delete_info(mid=None, tid=None):
    info = {
        'isFiles': 'false',
        't': {
            'id': '--',
            'opt': 'remove',
            'mid': '*' if mid is None else str(mid),
            'tid': ['*' if tid is None else str(tid)]
        }
    }
    return info


def _send_message(machines, info):
    import redis
    from judge_server.redis_connections import pool

    r = redis.Redis(connection_pool=pool)
    for name in machines:
        r.rpush(name, dumps(info))

    return len(machines)


@shared_task
def send_data_insert(mid=None, tid=None, machine_name=None, info=None):
    machines = _get_data_machines_to_inform(mid, tid, machine_name)

    _send_message(machines, info)
    return machines


@shared_task
def send_data_delete(mid=None, tid=None, machine_name=None):
    machines = _get_data_machines_to_inform(mid, tid, machine_name)
    info = _get_data_delete_info(mid, tid)
    print(info)
    _send_message(machines, info)
    return machines


def _get_code_machines_to_inform(mid=None, tid=None, machine_name=None):
    from judge.models import Machine
    from .models import Environment, SpecialJudge
    if mid is None:
        if machine_name is None:
            machines = {machine.data_queue for machine in Machine.objects.all()}
        else:
            machine = Machine.objects.get(name=machine_name)
            machines = {machine.name}
    else:
        envs = Environment.objects.filter(limit__problem__meta_problem_id=mid).distinct()
        machines = set()
        for env in envs:
            env_machines = env.machine.all()
            for machine in env_machines:
                machines.add(machine.name)
    return machines


def _get_unique_sub_queue_name(number, index):
    ret = ''
    for i in range(1, number+1):
        if i == index:
            ret += '1'
        else:
            ret += '0'
    return ret


def _send_code_message(machines, info):
    import redis
    from judge_server.redis_connections import pool
    from judge.models import Machine

    r = redis.Redis(connection_pool=pool)

    m_ok = machines
    print('m_ok', m_ok)
    q_send = []

    ms = Machine.objects.all()
    print('ms', ms)
    length = ms.count()
    i = 1
    i_send = dumps(info)
    for m in ms:
        print(m.name, m_ok, m.name in m_ok)
        if m.name in m_ok:
            name = _get_unique_sub_queue_name(length, i)
            q_send.append(name)
            r.rpush(name, i_send)
        i += 1

    return q_send


@shared_task
def send_code_insert(mid=None, tid=None, machine_name=None, info=None):
    machines = _get_code_machines_to_inform(mid, tid, machine_name)
    print(machines)
    q_send = _send_code_message(machines, info)
    return q_send


@shared_task
def send_code_delete(mid=None, tid=None, machine_name=None, info=None):
    machines = _get_code_machines_to_inform(mid, tid, machine_name)
    print(info)
    _send_code_message(machines, info)
    return machines
