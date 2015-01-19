import datetime
import logging
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WorkTask(Base):
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

    def __repr__(self):
        return "<WorkTask('{body:s}', '{jid:s}', '{task_type:s}', '{create_dt:s}', '{finish_dt:s}', '{handle_time:f}')>".format(self.__dict__)


class SendTask(Base):
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

    def __repr__(self):
        return "<WorkTask('{body:s}', '{jid:s}', '{task_type:s}', '{create_dt:s}', '{finish_dt:s}', '{handle_time:i}')>".format(self.__dict__)
 



class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)


class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True)


class CallStat(Base):
    __tablename__ = 'call_stats'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    resource = Column(String)
    call_dt = Column(DateTime)

    def __init__(self, user, resource):
        self.user = user
        self.resource = resource
        self.call_dt = datetime.datetime.utcnow()

class Category(Base):
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

        def __repr__(self):
        return "<Category('{name:s}', '{is_active:b}', '{add_dt:s}')>".format(**self.__dict__)

class Consultant(Base):
    __tablename__ = 'consultants'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class ConsultantCategory(Base):
    __table__ = 'consultant_categories'
    id = Column(Integer, primary_key=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, cons_id, cat_id):
        self.consultant_id = cons_id
        self.category_id = cat_id
        

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    from_jid = Column(String)
    category_id = Column(Integer) #foreign key
    create_dt = Column(DateTime)
 
    def __init__(self, message, from_jid, category):
        self.message = message
        self.from_jid = from_jid
        self.category = category
        self.create_dt = datetime.datetime.utcnow()

    def __repr__(self):
        return "<Question('{message:s}', '{from_jid:s}', '{category_id:i}', '{create_dt:s}')>".format(self.__dict__)
 

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
