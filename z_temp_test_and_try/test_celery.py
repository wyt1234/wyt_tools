from celery import Celery

app = Celery('tasks', broker='redis://localhost')


@app.task()
def add(x, y):
    print(x + y)


@app.task
def say(what):
    print(what)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls say('hello') every 10 seconds.
    sender.add_periodic_task(1.0, say.s('hello'), name='add every 10')

    # See periodic tasks user guide for more examples:
    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html


if __name__ == '__main__':
    # app.start()
    # add.delay(2, 8)
    say.delay('hello')
    # celery -A test_celery flower
    # celery -A test_celery worker --loglevel=info



