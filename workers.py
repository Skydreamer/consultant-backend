from multiprocessing import Process
import logging

class WorkerPool():
    def __init__(self, proc_num):
        self.worker_number = proc_num
        self.worker_count = 0

    def start_pool(self):
        pass

    def stop_pool(self):
        pass

class Worker(Process):
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        pass


