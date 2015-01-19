'''
Controllers
'''
import logging
import multiprocessing
import pool

HANDLER_WORK_COUNT = 40

class PoolController(object):
    '''
    PoolController
    '''
    def __init__(self, task_handler_queue, send_message_queue):
        '''
        Init
        '''
        self.task_handler_pool = pool.TaskHandlerPool(HANDLER_WORK_COUNT)
        self.server_bot_pool = pool.ServerBotPool()
        self.task_queue = task_handler_queue
        self.send_queue = send_message_queue
        self.state = False

    def start(self):
        '''
        Start
        '''
        if self.state is False:
            logging.info('Pool Controller - Start pools')
            self.state = True
            self.task_handler_pool.start(self.task_queue, self.send_queue)
            self.server_bot_pool.start(self.task_queue, self.send_queue)
            logging.info('Pool Controller - All pools are started')
        else:
            logging.debug('Pools are already started')

    def stop(self):
        '''
        Stop
        '''
        if self.state is True:
            logging.debug('Pool Controller - Stop pools')
            self.state = False
            self.task_handler_pool.stop()
            self.server_bot_pool.stop()
            logging.debug('Pool Controller - All pools are stopped')
        else:
            logging.debug('Pools are already stopped')

    def get_state(self):
        '''
        Get State
        '''
        task_pool_info = 'TaskHandlerPool:\n' + str(self.task_handler_pool.work_pool) + '\n'
        bot_pool_info = 'ServerBotPool:\n' + str(self.server_bot_pool.work_pool) + '\n'
        return task_pool_info + bot_pool_info


class QueueController(object):
    '''
    QueueController
    '''
    def __init__(self):
        '''
        Init
        '''
        self.task_handler_queue = multiprocessing.Queue()
        self.send_message_queue = multiprocessing.Queue()

    def get_state(self):
        '''
        Get State
        '''
        task_info = 'Task handler queue length = %i' % \
                        self.task_handler_queue.qsize() + '\n'
        send_info = 'Send handler queue length = %i' % \
                        self.send_message_queue.qsize() + '\n'
        return task_info + send_info
