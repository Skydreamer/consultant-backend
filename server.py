import os
import time
import sys
import optparse
import logging
from server_bots import ServerXMPPReceiveBot
import config

class ServerComponent():
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.bot_sender = None
        self.bot_receiver = None
        self.pool = None

        self._init_slaves()

    def _init_slaves(self):
        self.bot_receiver = ServerXMPPReceiveBot(config.BOT_RECEIVER_JID,
                                                 config.BOT_RECEIVER_PASSWD)
        self.bot_receiver.register_plugin('xep_0030') # Service Discovery
        self.bot_receiver.register_plugin('xep_0004') # Data Forms
        self.bot_receiver.register_plugin('xep_0060') # PubSub
        self.bot_receiver.register_plugin('xep_0199') # XMPP Ping
        
        if self.bot_receiver.connect((self.url, self.port)):
            logging.info('Bot-receiver succesfully connected to server')
            logging.info('Bot-receiver is processing...')
            self.bot_receiver.process(block=False)
        else:
            logging.error('Bot-receiver failed connection to server')
            assert False

    def run(self):
        time.sleep(20)
        self.bot_receiver.finish()


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

    
    opts, args = opt.parse_args()

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')
    logging.info('Got args: %s' % str(opts))

    return (opts, args)
    

if __name__ == '__main__':
    opts, args = parse_args()
    url = opts.url or ''
    port = opts.port or ''

    assert url, 'url needed'
    assert port, 'port needed'

    logging.info('Starting server...')
    server_component = ServerComponent(url, port)
    server_component.run()
    logging.info('Stopping server...')


