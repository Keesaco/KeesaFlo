# Analysis queue API.
import API.PALQueue as queue

def visualise(	filename ):
	queue.add_task('vis;' + filename)

def kill():
    queue.add_task('kill;' + filename)