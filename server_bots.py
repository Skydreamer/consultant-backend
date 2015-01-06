#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time
import pool
from task import Task

import sleekxmpp

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

    
class ServerXMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        self.name = jid.split('@')[0]
        self.connected = False
        self.session_start = False

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("connected", self.connect_handler)
        self.add_event_handler("disconnected", self.disconnect_handler)
        self.add_event_handler("session_start", self.session_start_handler)

    def disconnect_handler(self, event):
        logging.info('%s was disconnected' % self.name)
        self.connected = False
    
    def connect_handler(self, event):
        logging.info('%s was connected' % self.name)
        self.connected = True

    def session_start_handler(self, event):
        logging.info('%s was started' % self.name)
        self.send_presence()
        self.get_roster()
        self.session_start = True

    def disconnect_from_server(self):
        self.disconnect(wait=True)


class ServerXMPPReceiveBot(ServerXMPPBot):
    def __init__(self, jid, password, task_handler_queue):
        ServerXMPPBot.__init__(self, jid, password)
        self.add_event_handler("message", self.message_handler)
        self.task_handler_queue = task_handler_queue

    def message_handler(self, msg):
        logging.info('%s receive message: %s' % (self.name, str(msg.values)))
        msg_task = Task(msg.getFrom(), msg['body'], msg['type'])
        self.task_handler_queue.put(msg_task)
        

class ServerXMPPSendBot(ServerXMPPBot):
    def __init__(self, jid, password):
        ServerXMPPBot.__init__(self, jid, password)

    def send_msg(self, recipient, msg, type='chat'):
        logging.info('%s send to %s message: %s' % (self.name, recipient, msg))
        self.send_message(recipient, unicode(msg), mtype=type, mfrom=self.boundjid.jid)

    def _send_answers(self, to):
        for i in range(10):
            self.send_msg(to, unicode(i))
            time.sleep(1)
