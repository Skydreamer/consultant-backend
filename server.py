import os
import time
import sys
import optparse
import logging
import xmpp_bots
from utils import config
from utils.statistics import Statistics
import task
import pool
import controllers
import random
import gc


class ServerComponent():
    def __init__(self, url, port, db_params=None):
        self.connect_params = (url, int(port))
        self.database_params = db_params
        self.statistics = Statistics()
        self.db_controller = None 
        self.queue_controller = None
        self.pool_controller = None
        self.is_started = False

    def start(self):
        logging.info('Starting server...')
        self.db_controller = controllers.DatabaseController('database.db')
        self.queue_controller = controllers.QueueController()
        self.pool_controller = controllers.PoolController(self.connect_params,
                                    self.queue_controller.task_handler_queue, 
                                    self.queue_controller.send_message_queue, 
                                    self.db_controller)
        self.pool_controller.start()
        self.is_started = True
        logging.info('Server succesfully started!')

    def stop(self):
        logging.info('Stopping server...')
        self.pool_controller.stop()
        self.is_started = False
        logging.info('Server succesfully stopped!')

    def run(self):
        try:
            while True:
                message = unicode(raw_input())
                if message.startswith('quit'):
                    self.stop()
                    break 
                elif message.startswith('gc'):
                    print 'Collected %d' % gc.collect()
                elif message.startswith('stat'):
                    print self.pool_controller.get_state()
                    print self.queue_controller.get_state()
                    print self.statistics.avg_time()
                elif message.startswith('restart'):
                    logging.info('Restarting ServerComponent...')
                    self.stop()
                    self.start()
                    logging.info('Server succesfully restarted!')
                else:
                    message_list = message.split()
                    if len(message_list) == 2:
                        num = int(message_list[1])
                        message = message_list[0]
                    else:
                        num = random.randint(10, 30)
                    logging.info('Add task to send %d messages [%s]' % (num, message))
                    for i in range(num):
                        jid = random.choice(self.pool_controller.recv_message_pool.work_pool).jid
                        send_task = task.SendTask(jid, message)
                        self.queue_controller.send_message_queue.put(send_task)
        except KeyboardInterrupt:
            logging.info('Got KeyboardInterrupt... stopping server...')
            self.stop()


def parse_args():
    opt = optparse.OptionParser()

    opt.add_option('-q', '--quiet', help='set logging to ERROR',
                   action='store_const', dest='loglevel',
                   const=logging.ERROR, default=logging.INFO)
    opt.add_option('-d', '--debug', help='set logging to DEBUG',
                   action='store_const', dest='loglevel',
                   const=logging.DEBUG, default=logging.INFO)
    opt.add_option('-v', '--verbose', help='set logging to COMM',
                   action='store_const', dest='loglevel',
                   const=5, default=logging.INFO)
    opt.add_option('-u', '--url', help='jabber server url', dest='url',
                   default='89.189.106.3')
    opt.add_option('-p', '--port', help='jabber server port',
                   default='15222')

    opts, args = opt.parse_args()

    log_format = '%(asctime)s  [P%(process)s] %(levelname)-8s : %(module)s - %(message)s'
    logging.basicConfig(level=opts.loglevel, format=log_format)
    logging.info('Got args: %s' % str(opts))
    return (opts, args)
    

if __name__ == '__main__':
    opts, args = parse_args()
    url = opts.url
    port = opts.port
    assert url, 'url needed'
    assert port, 'port needed'
    server_component = ServerComponent(url, port)
    server_component.start()
    server_component.run()
