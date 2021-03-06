#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class EchoBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        print 'Session start'
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        print msg
        print "%(body)s" % msg


    """        
    def send_message(self, mto, mbody, msubject=None, mtype=None,
                     mhtml=None, mfrom=None, mnick=None):

        self.make_message(mto, mbody, msubject, mtype,
                          mhtml, mfrom, mnick).send()  """


if __name__ == '__main__':
    optp = OptionParser()

    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")

    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    opts.jid = "testuser@cons-jabber"

    opts.password = "1111"


    xmpp = EchoBot(opts.jid, opts.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    if xmpp.connect(('89.189.106.3', '15222')):
        xmpp.process(block=False)
        print 'Try to get receivers...'
        xmpp.send_message('server-recv001@cons-jabber', 'get_recvs')
        while True:
            msg_list = raw_input().split()
            if len(msg_list) == 2:
                message, num = msg_list
            else:
                message = msg_list[0]
                num = 1
            for i in range(int(num)):
                xmpp.send_message('server-recv001@cons-jabber', message)
    else:
        print("Unable to connect.")
