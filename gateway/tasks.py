from celery import Celery
from kombu import Queue
from queue import Empty
from functools import wraps

import aiohttp
import asyncio

app = Celery('tasks', broker='amqp://guest@localhost//')
app.conf.broker_connection_retry_on_startup = True

task_queues = [
    Queue('message'),
]

rate_limits = {
    'message': 10,
}

task_queues += [Queue(name+'_tokens', max_length=10) for name, limit in rate_limits.items()]

app.conf.task_queues = task_queues


@app.task
def token():
    return 1


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for name, limit in rate_limits.items():
        sender.add_periodic_task(
            1 / limit,
            token.signature(queue=name + '_tokens'),
            name=name + '_tokens')


def rate_limit(task_group):
    def decorator_func(func):
        @wraps(func)
        def function(self, *args, **kwargs):
            with self.app.connection_for_read() as conn:
                with conn.SimpleQueue(task_group+'_tokens', no_ack=True, queue_opts={'max_length': 2}) as queue:
                    try:
                        queue.get(block=True, timeout=1)
                        return func(self, *args, **kwargs)
                    except Empty:
                        self.retry(countdown=1)
        return function
    return decorator_func


async def send_async_request(data):
    url = "http://127.0.0.1:8002/process/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                response_data = await response.json()
                print(response_data)
    except Exception as e:
        print(f"Error: {e}")


@app.task(bind=True, max_retries=None)
@rate_limit('message')
def send_request(self, data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_async_request(data))
    loop.close()
    return {'status': 200}
