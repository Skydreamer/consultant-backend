import time


class Task:
    def __init__(self, address, body):
        self.address = address
        self.body = body
        self.create_time = time.time()
        self.handle_time = None

    def get_body(self):
        return self.body
       
    def __str__(self):
        return 'From %s, body %s, created %s' % (self.address, self.body, self.create_time)


class SendTask:
    def __init__(self, receiver, message):
        self.receiver = receiver
        self.message = message
        self.create_time = time.time()
        self.handle_time = None

    def __str__(self):
        return 'Send to %s, [%s]' % (self.receiver, self.message)
