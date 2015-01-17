# -*- coding: utf-8 -*-

import logging
import sleekxmpp

from utils import statistics
from models import WorkTask    

class ServerXMPPBot(sleekxmpp.ClientXMPP):
    '''
    ServerXMPPBot
    '''
    def __init__(self, jid, password):
        self.name = jid.split('@')[0]
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("connected", self.connect_handler)
        self.add_event_handler("disconnected", self.disconnect_handler)
        self.add_event_handler("session_start", self.session_start_handler)

        self.auto_authorize = True
        self.auto_reconnect = True

    def disconnect_handler(self, event):
        logging.info('[HANDLER] %s was disconnected' % self.name)
    
    def connect_handler(self, event):
        logging.info('[HANDLER] %s was connected' % self.name)

    def session_start_handler(self, event):
        logging.info('[HANDLER] %s session was started' % self.name)
        self.send_presence()
        self.get_roster()

    def disconnect_from_server(self):
        self.disconnect(wait=False)


class ServerXMPPReceiveBot(ServerXMPPBot):
    '''
    ServerXMPPReceiveBot
    '''
    def __init__(self, jid, password, task_handler_queue):
        ServerXMPPBot.__init__(self, jid, password)
        self.add_event_handler("message", self.message_handler)
        self.task_handler_queue = task_handler_queue

    def message_handler(self, msg):
        logging.debug('%s receive message: %s' % (self.name, str(msg.values)))
        work_task = WorkTask(msg.getFrom(), msg['body'])
        self.task_handler_queue.put(work_task)

class StatXMPPReceiveBot(ServerXMPPBot):
    '''
    ServerXMPPReceiveBot
    '''
    def __init__(self, jid, password, stats):
        super(StatXMPPReceiveBot, self).__init__(jid, password)
        seld.add_event_handler('message', self.message_handler)
        self.stats = statistics.Statistics() 

    def message_handler(self, msg):
        logging.debug('Got stat message: %s' % msg)
        

class ServerXMPPSendBot(ServerXMPPBot):
    '''
    ServerXMPPSendBot
    '''
    def __init__(self, jid, password):
        ServerXMPPBot.__init__(self, jid, password)
        self.add_event_handler("message", self.message_handler)

    def message_handler(self, msg):
        logging.debug('%s receive message: %s' % (self.name, str(msg.values)))
        msg.reply('CONFIRMED!')

    def send_msg(self, recipient, msg):
        logging.debug('%s send to %s message: %s' % (self.name, recipient, msg))
        self.send_message(recipient, msg)
