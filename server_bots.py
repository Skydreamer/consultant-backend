#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import getpass
from optparse import OptionParser
import threading
import time

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
        logging.info('%s was disconnected' % self.name)
        self.disconnect(wait=True)

    def send_msg(self, recipient, msg, type='chat'):
        logging.info('%s send to %s message: %s' % (self.name, recipient, msg))
        self.send_message(mto=recipient, mbody=msg, mtype=type)


class ServerXMPPReceiveBot(ServerXMPPBot):
    def __init__(self, jid, password):
        ServerXMPPBot.__init__(self, jid, password)
        self.add_event_handler("message", self.message_handler)

    def message_handler(self, msg):
        logging.info('%s receive message: %s' % (self.name, str(msg.values)))
        if msg['type'] in ('chat', 'normal'):	    
            print msg.getFrom()
            threading.Thread(target=self._send_answers, 
                             args=(msg.getFrom(),)).start()

    def _send_answers(self, to):
        for i in range(10):
            self.send_msg(to, unicode(i))
            time.sleep(1)

class ServerXMPPSendBot(ServerXMPPBot):
    def __init__(self, jid, password):
        ServerXMPPBot.__init__(self, jid, password)


