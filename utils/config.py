"""
Config file
"""

IP = '89.189.106.3'
PORT = '15222'
VIRTUAL_HOST = 'cons-jabber'

RECEIVER_BOTS = {
    'server-recv001@' + VIRTUAL_HOST : '111',
    #'server-recv002@' + VIRTUAL_HOST : '111',
    #'server-recv003@' + VIRTUAL_HOST : '111',
    #'server-recv004@' + VIRTUAL_HOST : '111',
}

SENDER_BOTS = {
    'server-send001@' + VIRTUAL_HOST : '111',
    'server-send002@' + VIRTUAL_HOST : '111',
    'server-send003@' + VIRTUAL_HOST : '111',
    'server-send004@' + VIRTUAL_HOST : '111',
    #'server-send005@' + VIRTUAL_HOST : '111',
    #'server-send006@' + VIRTUAL_HOST : '111',
    #'server-send007@' + VIRTUAL_HOST : '111',
    #'server-send008@' + VIRTUAL_HOST : '111',
    #'server-send009@' + VIRTUAL_HOST : '111',
    #'server-send010@' + VIRTUAL_HOST : '111',
}

QUEUE_GET_TIMEOUT = 10
CATEGORIES_LIST = 'utils/categories.txt'
