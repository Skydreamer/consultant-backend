import logging
import sqlalchemy
import models
from sqlalchemy.orm import sessionmaker

READ_OPERATIONS = [
    'get_messages',
    'get_consultants',
    'get_categories'
]

WRITE_OPERATIONS = [
    'ask_question',
    'send_chat_message'
]

class DatabaseManager(object):
    def __init__(self):
        #self.engine = sqlalchemy.create_engine('sqlite:///:memory:')    
        self.engine = sqlalchemy.create_engine('sqlite:///temp.db', echo=False)
        self.connection = self.engine.connect()
        self.session_maker = sessionmaker(bind=self.engine)
        self.create_all()
        
    def create_all(self):
        models.register_models(self.engine)

    def add_categories(self):
        models.create_categories(self.session_maker())
       
    def drop_all(self):
        models.unregister_models(self.engine)
    
    def get_session(self):
        return self.session_maker()
    
    
class CallStatController(object):
    def __init__(self):
        pass

    def __enter__(self):
        logging.debug('Enter into CallStatManager')

    def __exit__(self):
        logging.debug('Exit from CallStatManager')
