import time
import datetime
import logging
import sqlalchemy
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
        return str(self.__dict__)
        return "<WorkTask('{body}', '{jid}', '{task_type}', '{create_dt}', '{finish_dt}', '{handle_time}')>".format(self.__dict__)


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
        return "<WorkTask('{body}', '{jid}', '{task_type}', '{create_dt}', '{finish_dt}', '{handle_time}')>".format(self.__dict__)
        

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
    dt = Column(DateTime)

    def __init__(self, user, resource):
        self.user = user
        self.resource = resource
        self.dt = datetime.datetime.utcnow()

 
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
        return "<Question('{message}', '{from_jid}', '{category_id}', '{create_dt}')>".format(self.__dict__)
        

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
