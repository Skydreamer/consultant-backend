'''
Server
'''

import optparse
import logging
import database

from controllers import QueueController, PoolController
from utils.statistics import Statistics
from utils.misc import main_logger


class ServerComponent(object):
    '''
    ServerComponent
    '''
    def __init__(self):
        self.statistics = Statistics()
        self.db_controller = database.DatabaseManager()
        self.queue_controller = None
        self.pool_controller = None
        self.is_started = False

    def start(self):
        main_logger.info('Starting server...')
        self.db_controller.add_categories()
        self.queue_controller = QueueController()
        self.pool_controller = PoolController(
                            self.queue_controller.task_handler_queue,
                            self.queue_controller.send_message_queue)
        self.pool_controller.start()
        self.is_started = True
        main_logger.info('Server succesfully started!')

    def stop(self):
        main_logger.info('Stopping server...')
        self.pool_controller.stop()
        self.is_started = False
        main_logger.info('Server succesfully stopped!')

    def run(self):
        try:
            while True:
                message = unicode(raw_input())
                if message.startswith('quit'):
                    self.stop()
                    break
                elif message.startswith('stat'):
                    print self.pool_controller.get_state()
                    print self.queue_controller.get_state()
                    print self.statistics.avg_time()
                elif message.startswith('restart'):
                    main_logger.info('Restarting ServerComponent...')
                    self.stop()
                    self.start()
                    main_logger.info('Server succesfully restarted!')
                else:
                    main_logger.info('Wrong command')
        except KeyboardInterrupt:
            main_logger.info('Got KeyboardInterrupt... stopping server...')
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

    opts, args = opt.parse_args()

    log_format = '%(asctime)s  [P%(process)s] %(levelname)-8s : %(module)s - %(message)s'
    main_logger.info('Got args: %s' % str(opts))
    return (opts, args)


if __name__ == '__main__':
    opts, args = parse_args()
    server_component = ServerComponent()
    server_component.start()
    server_component.run()
