import subprocess
import config

REGISTER_CMD = 'sudo ejabberdctl register %s %s %s'

def register_users():
   users = dict(config.RECEIVER_BOTS.items() + config.SENDER_BOTS.items())
   for (login, passwd) in users.iteritems():
       username, host = login.split('@')
       print 'Register [%s]...' % username
       proc = subprocess.call(REGISTER_CMD % (username, host, passwd), shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    register_users()
