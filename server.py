import os
import time
import sys
import optparse
import logging
from server_bots import ServerXMPPReceiveBot, ServerXMPPSendBot
import config

class ServerComponent():
    def __init__(self, url, port, limits):
        self.url = url
        self.port = port
        self.bot_master = BotMaster(url, port, limits)
        self.pool = None

    def run(self):
        while True:
            message = unicode(raw_input())
            if message.startswith('quit'):
                self.bot_master.disconnect()
                break
            else:
                self.bot_master.send_broadcast(message)


class BotMaster():
    def __init__(self, url, port, limits):
        self.url = url
        self.port = port
        self.receive_bot_number, self.send_bot_number = limits
        self.send_bot_count, self.recv_bot_count = (0, 0)
        self.recv_bot_list = []
        self.send_bot_list = []
        
        self._init_slaves()
    
    def _init_slaves(self):
        logging.info('Initiate recv bots...')
        for (jid, passwd) in config.RECEIVER_BOTS.iteritems():
            logging.info('Initiate %s bot...' % jid)
            bot_receiver = ServerXMPPReceiveBot(jid, passwd)
            bot_receiver.register_plugin('xep_0030') # Service Discovery
            bot_receiver.register_plugin('xep_0004') # Data Forms
            bot_receiver.register_plugin('xep_0060') # PubSub
            bot_receiver.register_plugin('xep_0199') # XMPP Ping

            self.recv_bot_count += 1
            self.recv_bot_list.append(bot_receiver)
            
        logging.info('Initiate recv bots...')
        for(jid, passwd) in config.SENDER_BOTS.iteritems():
            logging.info('Initiate %s bot...' % jid)
            bot_sender = ServerXMPPSendBot(jid, passwd)
            bot_sender.register_plugin('xep_0030') # Service Discovery
            bot_sender.register_plugin('xep_0199') # XMPP Ping

            self.send_bot_count += 1
            self.send_bot_list.append(bot_sender)

        self.connect() 

    def connect(self):
        logging.info('Try to connect all bots to server...')
        bot_list = self.send_bot_list + self.recv_bot_list
        for bot in bot_list:
            if bot.connect((self.url, self.port)):
                logging.info('%s succesfully connected to server' % bot.name)
                logging.info('%s is processing...' % bot.name)
                bot.process(block=False)
            else:
                logging.error('%s failed connection to server' % bot.name)
                assert False

    def disconnect(self):
        logging.info('Try to disconnect all bots to server...')
        bot_list = self.send_bot_list + self.recv_bot_list
        for bot in bot_list:
            bot.disconnect_from_server()

    def send_broadcast(self, message):
        logging.info('Send message to receiver from all senders')
        for send_bot in self.send_bot_list:
            if send_bot.session_start:  
                send_bot.send_msg(self.recv_bot_list[0].jid, message)
            else:
                logging.info('Bot %s is not athorized' % send_bot.name)


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
                        format='%(asctime)s - %(name)s - %(levelname)-8s %(message)s')
    logging.info('Got args: %s' % str(opts))

    return (opts, args)
    

if __name__ == '__main__':
    opts, args = parse_args()
    url = opts.url or ''
    port = opts.port or ''
    recv_bot_number = opts.receivers
    send_bot_number = opts.senders
    limits = (recv_bot_number, send_bot_number)

    assert url, 'url needed'
    assert port, 'port needed'

    logging.info('Starting server...')
    server_component = ServerComponent(url, port, limits)
    server_component.run()
    logging.info('Stopping server...')


