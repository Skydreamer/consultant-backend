import os
import time
import sys
import optparse
import logging
from server_bots import ServerXMPPReceiveBot, ServerXMPPSendBot
import config
import task
import pool
import controllers
from task import Task, SendTask


class ServerComponent():
    def __init__(self, url, port):
        self.connect_params = (url, port)
        self.db_controller = controllers.DatabaseController('database.db')
        self.queue_controller = controllers.QueueController()
        self.pool_controller = controllers.PoolController(self.connect_params, self.queue_controller.task_handler_queue, self.queue_controller.send_message_queue, self.db_controller)
        self.pool_controller.start()

    def stop(self):
        logging.info('Stopping server...')
        self.pool_controller.stop()


    def run(self):
        while True:
            message = unicode(raw_input())
            if message.startswith('quit'):
                self.stop()
                break
            elif message.startswith('stat'):
                print self.pool_controller
            else:
                jid = self.pool_controller.recv_message_pool.work_pool[0].jid
                send_task = SendTask(jid, message)
                #send_task = SendTask('testuser@cons-jabber', message)
                num = 10
                logging.info('Add task to send %d messages [%s]' % (num, message))
                for i in range(num):
                    self.queue_controller.send_message_queue.put(send_task)


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
                   default='192.168.1.3')
    opt.add_option('-p', '--port', help='jabber server port',
                   default='5222')
    opt.add_option('-r', '--recievers', help='set number of recv bots',
                   dest='receivers', default=1)
    opt.add_option('-s', '--senders', help='set number of send bots',
                   dest='senders', default=10)

    
    opts, args = opt.parse_args()

    logging.basicConfig(level=opts.loglevel,
                        format='%(asctime)s  [P%(process)s] [T%(thread)s] - %(name)s - %(levelname)-8s %(message)s')
    logging.info('Got args: %s' % str(opts))

    return (opts, args)
    

if __name__ == '__main__':
    opts, args = parse_args()
    url = opts.url
    port = opts.port
    recv_bot_number = opts.receivers
    send_bot_number = opts.senders
    #TODO consider with limits
    limits = (recv_bot_number, send_bot_number)

    assert url, 'url needed'
    assert port, 'port needed'

    logging.info('Starting server...')
    server_component = ServerComponent(url, port)
    server_component.run()
    logging.info('Stopping server...')


