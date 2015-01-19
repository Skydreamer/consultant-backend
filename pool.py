'''
Pool
'''

import logging
import multiprocessing
import workers
from utils import config

class BasicPool(object):
    '''
    Basic Pool
    '''
    def __init__(self, work_num=None):
        self.worker_number = work_num
        if not self.worker_number:
            self.worker_number = multiprocessing.cpu_count() * 2
        self.name = ''
        self.work_pool = []

    def stop(self):
        logging.info('Stopping [%s]...' % self.name)
        for worker in self.work_pool:
            logging.info('Stopping [%s]...' % worker.name)
            worker.stop()
            worker.terminate()


class ServerBotPool(BasicPool):
    '''
    Server Bot Pool
    '''
    def __init__(self):
        super(ServerBotPool, self).__init__(len(config.RECEIVER_BOTS.keys()))
        self.name = 'ServerBotPool'

    def start(self, task_queue, send_queue):
        logging.info('Starting ServerBotPool with %i workers...' % self.worker_number)
        for (jid, passwd) in config.RECEIVER_BOTS.iteritems():
            worker = workers.ServerBotWorker(jid, passwd,
                                             task_queue, send_queue)
            worker.init_worker()
            worker.start()
            self.work_pool.append(worker)
            logging.debug('Process start: %s [%s]' % (worker.name, worker.pid))


class TaskHandlerPool(BasicPool):
    '''
    Task Handler Pool
    '''
    def __init__(self, worker_num):
        super(TaskHandlerPool, self).__init__()
        self.name = 'TaskHandlerPool'
        self.worker_number = worker_num

    def start(self, task_queue, send_queue):
        logging.info('Starting TaskHandlerPool with %i workers...' % self.worker_number)
        for i in range(self.worker_number):
            worker = workers.TaskHandler(task_queue, send_queue)
            worker.start()
            self.work_pool.append(worker)
            logging.debug('Process start: %s [%s]' % (worker.name, worker.pid))

