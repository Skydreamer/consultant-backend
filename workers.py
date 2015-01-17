import multiprocessing
import logging
import utils.config
import time
import xmpp_bots
import models
import database

from utils.statistics import Statistics
from multiprocessing.queues import Empty


class BasicWorker(multiprocessing.Process, object):
    def __init__(self):
        super(BasicWorker, self).__init__()
        self.process = multiprocessing.current_process()
        self.work = True


class TaskHandler(BasicWorker):
    def __init__(self, task_handler_queue, send_message_queue):
        super(TaskHandler, self).__init__()
        self.task_queue = task_handler_queue
        self.send_queue = send_message_queue
        self.statistics = Statistics()

    def stop(self):
        logging.debug('Turn off')
        self.work = False
        
    def run(self):
        self.db_manager = database.DatabaseManager()
        self.session = self.db_manager.get_session()
        logging.info('Process %s is ready to work' % self.name)
        get_timeout = utils.config.QUEUE_GET_TIMEOUT
        while self.work:
            try:
                logging.debug('%s is trying to get a task...' % self.name)
                task = self.task_queue.get(block=True, timeout=get_timeout)
                logging.info('%s got task [%s]' % (self.name,
                                                   str(task)))
                self.handle_task(task)
            except Empty:
                logging.debug('%s timeouted...' % self.name)
        logging.info('Process %s is ending...' % self.name)

    def handle_task(self, work_task):
        message = work_task.body
        send_task = None
        if message == 'get_categories':
            send_task = models.SendTask(work_task.jid, 'CATEGORY LIST')
        elif message == 'get_recvs':
            send_task = models.SendTask(work_task.jid, str(utils.config.RECEIVER_BOTS.keys()))
        elif message == 'get_sends':
            send_task = models.SendTask(work_task.jid, str(utils.config.SENDER_BOTS.keys()))
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
        #self.statistics.add_call(task.handle_time)
        logging.info('Handle task [%f] seconds...' % work_task.handle_time)


class BasicBotWorker(BasicWorker):
    def __init__(self, jid, passwd, conn_params):
        super(BasicBotWorker, self).__init__()
        self.work_bot = None
        self.jid = jid
        self.passwd = passwd
        self.conn_params = conn_params

    def xmpp_connect(self):    
        if self.work_bot.connect(self.conn_params, use_tls=False):
            logging.info('%s succesfully connected to server' % self.work_bot.name)
        else:
            logging.error('%s failed connection to server' % self.work_bot.name)
            assert False

    def xmpp_disconnect(self):
        logging.info('%s trying to disconnect from server...' % self.work_bot.name)
        self.work_bot.disconnect_from_server()
        
    def stop(self):
        self.work = False
        self.xmpp_disconnect()


class RecvBotWorker(BasicBotWorker):
    def __init__(self, jid, passwd, conn_params, task_handler_queue):
        super(RecvBotWorker, self).__init__(jid, passwd, conn_params)
        self.queue = task_handler_queue

    def init_worker(self):
        logging.info('Init xmpp worker')
        self.work_bot = xmpp_bots.ServerXMPPReceiveBot(self.jid, self.passwd, self.queue)
        self.work_bot.register_plugin('xep_0030') # Service Discovery
        self.work_bot.register_plugin('xep_0004') # Data Forms
        self.work_bot.register_plugin('xep_0060') # PubSub
        self.work_bot.register_plugin('xep_0199') # XMPP Ping
        self.xmpp_connect()

    def run(self):
        self.init_worker()
        logging.info('Process %s is ready to work' % self.name)
        logging.info('%s is processing...' % self.work_bot.name)
        self.work_bot.process(block=True)
        logging.info('Process %s is ending...' % self.name)


class SendBotWorker(BasicBotWorker):
    def __init__(self, jid, passwd, conn_params, send_message_queue):
        super(SendBotWorker, self).__init__(jid, passwd, conn_params)
        self.queue = send_message_queue

    def init_worker(self):
        logging.info('Init xmpp worker')
        self.work_bot = xmpp_bots.ServerXMPPSendBot(self.jid, self.passwd)
        self.work_bot.register_plugin('xep_0030') # Service Discovery
        self.work_bot.register_plugin('xep_0004') # Data Forms
        self.work_bot.register_plugin('xep_0060') # PubSub
        self.work_bot.register_plugin('xep_0199') # XMPP Ping
        self.xmpp_connect()
        self.work_bot.process(block=False)

    def run(self):
        self.init_worker()
        logging.info('Process %s is ready to work' % self.name)
        while self.work:
            try:
                logging.debug('%s is trying to get a task...' % self.name)
                task = self.queue.get(block=True, timeout=utils.config.QUEUE_GET_TIMEOUT)
                logging.info('%s got task [%s, %s]' % (self.name, task.jid, task.body))
                self.work_bot.send_msg(task.jid, task.body)
                task.finish()
            except Empty:
                logging.debug('%s timeouted...' % self.name)
        logging.info('Process %s is ending...' % self.name)
