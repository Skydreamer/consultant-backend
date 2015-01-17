import logging
import multiprocessing
import pool
import sqlite3
import os
from utils import config

HANDLER_WORK_COUNT = 16

class PoolController(object):
    def __init__(self, conn_params, task_handler_queue, send_message_queue):
        self.task_handler_pool = pool.TaskHandlerPool(HANDLER_WORK_COUNT)
        self.send_message_pool = pool.SendMessagesPool() 
        self.recv_message_pool = pool.RecvMessagesPool()
        self.conn_params = conn_params
        self.task_queue = task_handler_queue
        self.send_queue = send_message_queue
        self.state = False

    def start(self):
        if self.state is False:
            logging.info('Pool Controller - Start pools')
            self.state = True
            self.task_handler_pool.start(self.task_queue, self.send_queue)
            self.send_message_pool.start(self.conn_params, self.send_queue)
            self.recv_message_pool.start(self.conn_params, self.task_queue)
            logging.info('Pool Controller - All pools are started')
        else:
            logging.debug('Pools are already started')

    def stop(self):
        if self.state is True:
            logging.debug('Pool Controller - Stop pools')
            self.state = False
            self.task_handler_pool.stop()
            self.send_message_pool.stop()
            self.recv_message_pool.stop()
            logging.debug('Pool Controller - All pools are stopped')
        else:
            logging.debug('Pools are already stopped')

    def get_state(self):
        task_info = 'TaskHandlerPool:\n' + str(self.task_handler_pool.work_pool) + '\n'
        send_info = 'SendMessagePool:\n' + str(self.send_message_pool.work_pool) + '\n'
        recv_info = 'RecvMessagePool:\n' + str(self.recv_message_pool.work_pool) + '\n'
        return task_info + send_info + recv_info


class QueueController(object):
    def __init__(self):
        self.task_handler_queue = multiprocessing.Queue()
        self.send_message_queue = multiprocessing.Queue()

    def get_state(self):
        task_info = 'Task handler queue length = %i' % \
                        self.task_handler_queue.qsize() + '\n'
        send_info = 'Send handler queue length = %i' % \
                        self.send_message_queue.qsize() + '\n'
        return task_info + send_info
