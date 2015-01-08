import logging
import multiprocessing
import workers
import config


class BasicPool(object):
    def __init__(self, work_num=None):
        self.worker_number = work_num
        if not self.worker_number:
            self.worker_number = multiprocessing.cpu_count() * 2
        self.name = ''
        self.work_pool = []

    #TODO abstract classes
    def start(self):
        raise Exception

    def stop(self):
        logging.info('Stopping [%s]...' % self.name) 
        for worker in self.work_pool:
            logging.info('Stopping [%s]...' % worker.name)
            worker.stop()
            worker.terminate()


class SendMessagesPool(BasicPool):
    def __init__(self):
        super(SendMessagesPool, self).__init__()
        self.name = 'SendMessagesPool'
        
    def start(self, conn_params, queue):
        logging.info('Starting SendMessagePool with %i workers...' % self.worker_number)
        for (jid, passwd) in config.SENDER_BOTS.iteritems():
            worker = workers.SendBotWorker(jid, passwd, conn_params, queue)
            worker.init_worker()
            worker.start()
            self.work_pool.append(worker)
            logging.debug('Process start: %s [%s]' % (worker.name, worker.pid))
        

class RecvMessagesPool(BasicPool):
    def __init__(self):
        super(RecvMessagesPool, self).__init__()
        self.name = 'RecvMessagesPool'
        
    def start(self, conn_params, queue):
        logging.info('Starting RecvMessagePool with %i workers...' % self.worker_number)
        for (jid, passwd) in config.RECEIVER_BOTS.iteritems():
            worker = workers.RecvBotWorker(jid, passwd, conn_params, queue)
            worker.init_worker()
            worker.start()
            self.work_pool.append(worker)
            logging.debug('Process start: %s [%s]' % (worker.name, worker.pid))

class TaskHandlerPool(BasicPool):
    def __init__(self):
        super(TaskHandlerPool, self).__init__()
        self.name = 'TaskHandlerPool'

    def start(self, task_queue, send_queue, db_controller):
        logging.info('Starting TaskHandlerPool with %i workers...' % self.worker_number)
        for i in range(self.worker_number):
            worker = workers.TaskHandler(task_queue, send_queue, db_controller)
            worker.start()
            self.work_pool.append(worker)
            logging.debug('Process start: %s [%s]' % (worker.name, worker.pid))

