"""
Config file
"""

VIRTUAL_HOST = 'cons-jabber'

RECEIVER_BOTS = {
    'server-recv001@' + VIRTUAL_HOST : '111',
    'server-recv002@' + VIRTUAL_HOST : '111',
    'server-recv003@' + VIRTUAL_HOST : '111',
    'server-recv004@' + VIRTUAL_HOST : '111',
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


QUEUE_GET_TIMEOUT = 60

URL = '192.168.1.3'
PORT = '5222'

ADD_QUESTION_QUERY = """
insert into questions (message, sender)
values (?, ?);
"""

CREATE_TABLES = """
create table questions (
    id integer primary key autoincrement,
    create_dt timestamp default current_timestamp,
    message varchar(254) not null,
    from varchar(60) not null
);
"""
