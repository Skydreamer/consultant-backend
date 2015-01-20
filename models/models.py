import datetime
import logging
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey

# make it as sep class
Base = declarative_base()

class DeclarativeBase():
    def __init__(self):
        pass

    def __repr__(self):
        printed = {k: v for k, v in self.__dict__.iteritems() if k in self.__class__.__dict__}
        print printed
        #return "<WorkTask('{body:s}', '{jid:s}', '{task_type:s}', '{create_dt:s}', '{finish_dt:s}', '{handle_time:f}')>".format(self.__dict__)


class WorkTask(Base, DeclarativeBase):
    __tablename__ = 'work_tasks'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    jid = Column(String)
    task_type = Column(String)
    create_dt = Column(DateTime)
    finish_dt = Column(DateTime)
    handle_time = Column(Integer)

    def __init__(self, sender, body):
        self.body = body
        self.jid = str(sender)
        self.task_type = 'work_task'
        self.create_dt = datetime.datetime.utcnow()
        self.finish_dt = None
        self.handle_time = None

    def finish(self):
        self.finish_dt = datetime.datetime.utcnow()
        self.handle_time = (self.finish_dt - self.create_dt).total_seconds()


class SendTask(Base, DeclarativeBase):
    __tablename__ = 'send_tasks'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    jid = Column(String)
    task_type = Column(String)
    create_dt = Column(DateTime)
    finish_dt = Column(DateTime)
    handle_time = Column(Integer)
        
    def __init__(self, receiver, body):
        self.body = body
        self.jid = str(receiver)
        self.task_type = 'send_task'
        self.create_dt = datetime.datetime.utcnow()
        self.finish_dt = None
        self.handle_time = None

    def finish(self):
        self.finish_dt = datetime.datetime.utcnow()
        self.handle_time = (self.finish_dt - self.create_dt).total_seconds()

    def get_info(self):
        return (self.jid, self.body)


class Chat(Base, DeclarativeBase):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    consultant_id = Column(Integer, ForeignKey('consultants.id'))
    create_dt = Column(DateTime)

    def __init__(self, question_id, consultant_id):
        self.question_id = question_id
        self.consultant_id = consultant_id
        self.create_dt = datetime.datetime.utcnow()


class ChatMessage(Base, DeclarativeBase):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    message = Column(String)
    create_dt = Column(DateTime)
    
    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message
        self.create_dt = datetime.datetime.utcnow()


class CallStat(Base, DeclarativeBase):
    __tablename__ = 'call_stats'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    resource = Column(String)
    call_dt = Column(DateTime)

    def __init__(self, user, resource):
        self.user = user
        self.resource = resource
        self.call_dt = datetime.datetime.utcnow()


class Category(Base, DeclarativeBase):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean)
    add_dt = Column(DateTime)
 
    def __init__(self, name):
        self.name = name
        self.is_active = True
        self.add_dt = datetime.datetime.utcnow()

    def disable(self):
        self.is_active = False


class Consultant(Base, DeclarativeBase):
    __tablename__ = 'consultants'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


#class ConsultantCategory(Base, DeclarativeBase):
#    __table__ = 'consultant_categories'
#    id = Column(Integer, primary_key=True)
#    consultant_id = Column(Integer, ForeignKey('consultants.id'))
#    category_id = Column(Integer, ForeignKey('categories.id'))
#
#    def __init__(self, cons_id, cat_id):
#        self.consultant_id = cons_id
#        self.category_id = cat_id
#        
#    def __repr__(self):
#        return "<Category('{name:s}', '{is_active:b}', '{add_dt:s}')>".format(**self.__dict__)


class Question(Base, DeclarativeBase):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    from_jid = Column(String)
    category_id = Column(Integer) #foreign key
    create_dt = Column(DateTime)
    is_active = Column(Boolean)
 
    def __init__(self, message, from_jid, category_id):
        self.message = message
        self.from_jid = from_jid
        self.category_id = category_id
        self.create_dt = datetime.datetime.utcnow()
        self.is_active = True
    
    def close(self):
        pass


_models = [WorkTask, SendTask, Question, Category, Chat, ChatMessage]

def register_models(engine):
    logging.debug('Models: {0}'.format(repr(_models)))
    for model in _models:
        model.metadata.create_all(engine)

def unregister_models(engine):
    logging.debug('Drop all models')
    for model in _models:
        model.metadata.drop_all(engine)

def create_categories(session):
    logging.debug('Create categories')
    with open('utils/categories.txt') as cat_file:
        for row in cat_file:
            category = Category(unicode(row.strip()))
            session.add(category)
    session.commit()
