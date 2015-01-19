# -*- coding: utf-8 -*-
'''
XMPP Bots
'''
import logging
import sleekxmpp

from models import WorkTask

class ServerXMPPBot(sleekxmpp.ClientXMPP):
    '''
    ServerXMPPBot
    '''
    def __init__(self, jid, password, task_queue):
        self.name = jid.split('@')[0]
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("connected", self.connect_handler)
        self.add_event_handler("disconnected", self.disconnect_handler)
        self.add_event_handler("session_start", self.session_start_handler)
        self.add_event_handler("message", self.message_handler)

        self.auto_authorize = True
        self.auto_reconnect = True
        self.task_queue = task_queue
        self.protokol = None

    def message_handler(self, message):
        logging.debug('%s receive message: %s' % (self.name, str(message.values)))
        work_task = WorkTask(message.getFrom(), message['body'])
        self.task_queue.put(work_task)

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

    def send_msg(self, recipient, msg):
        logging.debug('%s send to %s message: %s' % (self.name, recipient, msg))
        self.send_message(recipient, msg)

