import logging
import sqlalchemy
import models
from sqlalchemy.orm import sessionmaker


class DatabaseManager(object):
    def __init__(self):
        #self.engine = sqlalchemy.create_engine('sqlite:///:memory:')    
        self.engine = sqlalchemy.create_engine('sqlite:///temp.db')
        self.connection = self.engine.connect()
        self.session_maker = sessionmaker(bind=self.engine)
        self.create_all()
        
    def create_all(self):
        models.register_models(self.engine)
       
    def drop_all(self):
        models.unregister_models(self.engine)
    
    def get_session(self):
        return self.session_maker()
    
    
class CallStatController(object):
    def __init__(self):
        pass
