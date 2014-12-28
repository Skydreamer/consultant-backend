import multiprocessing
from multiprocessing.queues import Empty
import logging
import config
import time

class WorkerPool():
    def __init__(self):
        self.worker_number = multiprocessing.cpu_count() * 2
        self.worker_count = 0
        self.work_queue = multiprocessing.Queue()
        self.work_pool = []
        self.start_pool()

    def start_pool(self):
        logging.info('Starting working pool with %i workers...' % self.worker_number)
        for i in range(self.worker_number):
            worker = Worker(self.work_queue)
            self.work_pool.append(worker)
            worker.start()

    def add_task(self, task):
        logging.info('Add task to pool queue: %s' % str(task))
        self.work_queue.put(task)

    def stop_pool(self):
        logging.info('Stopping working pool...')
        for worker in self.work_pool:
            worker.work = False
            worker.join()


class Worker(multiprocessing.Process):
    def __init__(self, queue):
        self.queue = queue
        self.work = True
        self.process = multiprocessing.current_process()
        self.name = '[%s] - #%s' % (self.process.pid, self.process.name)
        super(Worker, self).__init__()

    def run(self):
        logging.info('Process %s is ready to work' % self.name)
        while self.work:
            try:
                logging.debug('%s is trying to get a task...' % self.name)
                task = self.queue.get(block=True, timeout=config.QUEUE_GET_TIMEOUT)
                logging.info('%s got task [%s], type : %s' % (self.name, 
                                                              task.get_body(), 
                                                              task.type))
                if task.type == 'chat':
                    time.sleep(10)

            except Empty:
                logging.debug('%s timeouted...' % self.name)
        logging.info('Process %s is ending...' % self.name)


