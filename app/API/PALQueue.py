# Analsis queue PAL.
from google.appengine.api import taskqueue

def add_task( task ):
    q = taskqueue.Queue('jobs')
    tasks = []
    tasks.append(taskqueue.Task(payload = task, method = 'PULL'))
    q.add(tasks)
