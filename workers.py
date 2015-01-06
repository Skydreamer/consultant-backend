import multiprocessing
from multiprocessing.queues import Empty
import logging
import config
import time
import server_bots
from task import SendTask


class BasicWorker(multiprocessing.Process, object):
    def __init__(self):
        super(BasicWorker, self).__init__()
        self.work = True
        self.process = multiprocessing.current_process()


class TaskHandler(BasicWorker):
    def __init__(self, task_handler_queue, send_message_queue, db_controller):
        super(TaskHandler, self).__init__()
        self.task_queue = task_handler_queue
        self.send_queue = send_message_queue
        self.db_controller = db_controller

    def stop(self):
        logging.debug('Turn off')
        self.work = False
        
    def run(self):
        logging.info('Process %s is ready to work' % self.name)
        get_timeout = config.QUEUE_GET_TIMEOUT
        while self.work:
            try:
                logging.info('%s is trying to get a task...' % self.name)
                task = self.task_queue.get(block=True, timeout=get_timeout)
                logging.info('%s got task [%s]' % (self.name,
                                                   str(task)))
                self.handle_task(task)
            except Empty:
                logging.info('%s timeouted...' % self.name)
        logging.info('Process %s is ending...' % self.name)

    def handle_task(self, task):
        message = task.body
        if message == 'chat':
            time.sleep(10)
        elif message == 'get_categories':
            sendTask = SendTask(task.address, 'CATEGORY LIST', 'get_categories_answer')
            self.send_queue.put(sendTask)
        elif message == 'question':
            self.db_controller.add_question(message, task.address)
        

class BasicBotWorker(BasicWorker):
    def __init__(self, jid, passwd, conn_params):
        super(BasicBotWorker, self).__init__()
        self.work_bot = None
        self.jid = jid
        self.passwd = passwd
        self.conn_params = conn_params

    def connect(self):    
        if self.work_bot.connect(self.conn_params):
            logging.info('%s succesfully connected to server' % self.work_bot.name)
        else:
            logging.error('%s failed connection to server' % self.work_bot.name)
            assert False

    def disconnect(self):
        logging.info('%s trying to disconnect from server...' % self.work_bot.name)
        self.work_bot.disconnect_from_server()
        
    def stop(self):
        self.work = False
        self.disconnect()


class RecvBotWorker(BasicBotWorker):
    def __init__(self, jid, passwd, conn_params, task_handler_queue):
        super(RecvBotWorker, self).__init__(jid, passwd, conn_params)
        self.queue = task_handler_queue

    def init_worker(self):
        self.work_bot = server_bots.ServerXMPPReceiveBot(self.jid, self.passwd, self.queue)
        self.work_bot.register_plugin('xep_0030') # Service Discovery
        self.work_bot.register_plugin('xep_0004') # Data Forms
        self.work_bot.register_plugin('xep_0060') # PubSub
        self.work_bot.register_plugin('xep_0199') # XMPP Ping
        self.connect()

    def run(self):
        logging.info('Process %s is ready to work' % self.name)
        logging.info('%s is processing...' % self.work_bot.name)
        self.work_bot.process(block=True)
        logging.info('Process %s is ending...' % self.name)


class SendBotWorker(BasicBotWorker):
    def __init__(self, jid, passwd, conn_params, send_message_queue):
        super(SendBotWorker, self).__init__(jid, passwd, conn_params)
        self.queue = send_message_queue

    def init_worker(self):
        self.work_bot = server_bots.ServerXMPPSendBot(self.jid, self.passwd)
        self.work_bot.register_plugin('xep_0030') # Service Discovery
        self.work_bot.register_plugin('xep_0199') # XMPP Ping
        self.connect()
        self.work_bot.process(block=False)

    def run(self):
        logging.info('Process %s is ready to work' % self.name)
        while self.work:
            try:
                logging.info('%s is trying to get a task...' % self.name)
                task = self.queue.get(block=True, timeout=config.QUEUE_GET_TIMEOUT)
                logging.info('%s got task [%s]' % (self.name,
                                                   str(task)))
                self.work_bot.send_msg(task.receiver, task.message, task.type)
            except Empty:
                logging.info('%s timeouted...' % self.name)
        logging.info('Process %s is ending...' % self.name)
