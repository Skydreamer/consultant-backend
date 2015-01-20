'''
WORKERS
'''

import multiprocessing
import logging
import utils.config
import time
import xmpp_bots
import models
import database

from multiprocessing.queues import Empty
from utils.misc import main_logger, task_logger


class BasicWorker(multiprocessing.Process, object):
    '''
    BasicWorker
    '''
    def __init__(self):
        super(BasicWorker, self).__init__()
        self.db_manager = database.DatabaseManager()
        self.session = self.db_manager.get_session()
        self.process = multiprocessing.current_process()
        self.work = True


class TaskHandler(BasicWorker):
    '''
    TaskHandler
    '''
    def __init__(self, task_handler_queue, send_message_queue):
        super(TaskHandler, self).__init__()
        self.task_queue = task_handler_queue
        self.send_queue = send_message_queue

    def stop(self):
        main_logger.debug('Turn off')
        self.work = False

    def run(self):
        task_logger.info('Process %s is ready to work' % self.name)
        main_logger.info('Process %s is ready to work' % self.name)
        get_timeout = utils.config.QUEUE_GET_TIMEOUT
        while self.work:
            try:
                task_logger.info('%s is trying to get a task...' % self.name)
                task = self.task_queue.get(block=True, timeout=get_timeout)
                task_logger.info('%s got task [%s]' % (self.name,
                                                   str(task)))
                self.handle_task(task)
            except Empty:
                task_logger.info('%s timeouted...' % self.name)
        task_logger.info('Process %s is ending...' % self.name)
        main_logger.info('Process %s is ready to work' % self.name)

    def handle_task(self, work_task):
        message = work_task.body
        send_task = None
        if message == 'get_categories':
            data = '|'.join(map(str, self.db_manager.get_session().query(models.models.Category).all()))
            send_task = models.SendTask(work_task.jid, data)
        elif message == 'get_recvs':
            send_task = models.SendTask(work_task.jid,
                                str(utils.config.RECEIVER_BOTS.keys()))
        elif message == 'get_sends':
            send_task = models.SendTask(work_task.jid,
                                str(utils.config.SENDER_BOTS.keys()))
        elif message == 'question':
            question = models.Question(message, work_task.jid, 777)
            self.session.add(question)
            self.session.commit()
            send_task = models.SendTask(work_task.jid, str(question.id))
        else:
            time.sleep(1)

        self.session.add(work_task)
        if send_task:
            self.session.add(send_task)
            self.send_queue.put(send_task)

        work_task.finish()
        self.session.commit()
        main_logger.info('Handle task [%f] seconds...' % work_task.handle_time)


class ServerBotWorker(BasicWorker):
    '''
    ServerBotWorker
    '''
    def __init__(self, jid, passwd, task_queue, send_queue):
        super(ServerBotWorker, self).__init__()
        self.work_bot = None
        self.jid = jid
        self.passwd = passwd
        self.conn_params = (utils.config.IP, utils.config.PORT)
        self.task_queue = task_queue
        self.send_queue = send_queue

    def xmpp_connect(self):
        if self.work_bot.connect(self.conn_params, use_tls=False):
            main_logger.info('%s succesfully connected to server' % self.work_bot.name)
        else:
            main_logger.error('%s failed connection to server' % self.work_bot.name)
            assert False

    def xmpp_disconnect(self):
        main_logger.info('%s trying to disconnect from server...' % self.work_bot.name)
        self.work_bot.disconnect_from_server()

    def stop(self):
        self.work = False
        self.xmpp_disconnect()

    def init_worker(self):
        main_logger.info('Init xmpp worker')
        self.work_bot = xmpp_bots.ServerXMPPBot(self.jid, self.passwd,
                                                self.task_queue)
        self.work_bot.register_plugin('xep_0030') # Service Discovery
        self.work_bot.register_plugin('xep_0004') # Data Forms
        self.work_bot.register_plugin('xep_0060') # PubSub
        self.work_bot.register_plugin('xep_0199') # XMPP Ping
        self.xmpp_connect()
        self.work_bot.process(block=False)

    def run(self):
        self.init_worker()
        main_logger.info('Process %s is ready to work' % self.name)
        task_logger.info('Process %s is ready to work' % self.name)
        while self.work:
            try:
                task_logger.debug('%s is trying to get a task...' % self.name)
                send_task = self.send_queue.get(block=True, timeout=utils.config.QUEUE_GET_TIMEOUT)
                task_logger.info('%s got send task [%s, %s]' % (self.name, send_task.jid, send_task.body))
                self.work_bot.send_msg(send_task.jid, send_task.body)
                send_task.finish()
            except Empty:
                task_logger.debug('%s timeouted...' % self.name)
        task_logger.info('Process %s is ending...' % self.name)
        main_logger.info('Process %s is ending...' % self.name)


