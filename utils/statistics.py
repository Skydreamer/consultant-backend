import logging


class Statistics:
    _dict = {
        'task_count' : 0,
        'total_handler_time' : 0.0,
    }

    def __init__(self):
        self.__dict__ = Statistics._dict

    def add_call(self, time):
        logging.info('Add call with %f time' % time)
        self.task_count += 1
        self.total_handler_time += time

    def avg_time(self):
        try:
            return self.task_count / self.total_handler_time
        except ZeroDivisionError:
            return 'Stat is empty - 0.0'
