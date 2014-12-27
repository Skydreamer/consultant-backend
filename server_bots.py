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

def send_answers(bot, to):
    for i in range(10):
	bot.send_message(mto=to,
			 mbody=str(i),
			 mtype=u'GIVE ANSWER')
	time.sleep(1)
    
class ServerXMPPBot(sleekxmpp.ClientXMPP):
    def __init__(self, name, jid, password):
        self.name = name
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
    
    def start(self, event):
        logging.info('%s was started' % self.name)
        self.send_presence()
        
    def finish(self):
        logging.info('%s was disconnected')
        self.disconnect(wait=True)

class ServerXMPPReceiveBot(ServerXMPPBot):
    def __init__(self, jid, password):
        ServerXMPPBot.__init__(self, 'bot-receiver', jid, password)
        self.add_event_handler("message", self.message)

    def message(self, msg):
        logging.debug('Receive message: %s' % str(msg.values))
    
        if msg['type'] in ('chat', 'normal'):	    
            threading.Thread(target=send_answers, args=(self, msg.getFrom())).start()
