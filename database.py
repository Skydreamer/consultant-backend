import logging
import sqlalchemy


class DatabaseConnectionController(object):
    def __init__(self, filename):
        self.filename = filename
        self.connection = None
        if not os.path.exists(self.filename):
            logging.error('Need to create schema!')
        self.connect()

    def create_schema(self):
        pass

    def update_schema(self):
        pass

    def dump_data(self):
        pass

    def uploat_data(self):
        pass
        
    def connect(self):
        logging.info('Trying connect to sqlite3 database...')
        self.connection = sqlite3.connect(self.filename)


class DatabaseDataController(object):
    def __init__(self, db_conn_controller):
        self.db_connection = db_conn_controller

    def add_question(self):
        cursor = self.connection.cursor()
        cursor.execute(config.ADD_QUESTION_QUERY, (str(question), str(sender)))
        self.connection.commit()
        answer_id = cursor.lastrowid
        logging.info('Add question [%s] to the table (id:%i)' % (question, answer_id))
        return answer_id

    def get_question(self):
        pass

    def add_category(self):
        pass

    def get_categories(self):
        pass

    def _update_categories(self):
        pass

    def add_consultant(self):
        pass

    def get_consultant(self):
        pass

    def add_chat_message(self):
        pass

    def get_user_chat_history(self):
        pass

    def get_user_questions(self):
        pass

    
class CallStatController(object):
    def __init__(self):
        pass
