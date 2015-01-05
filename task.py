class Task:
    def __init__(self, address, body, type):
        self.address = address
        self.body = body
        self.type = type

    def get_body(self):
        return self.body
       
    def __str__(self):
        return 'From %s, type %s, body %s' % (self.address, self.type, self.body)


class SendTask:
    def __init__(self, receiver, message, type):
        self.receiver = receiver
        self.message = message
        self.type = type

    def __str__(self):
        return 'Send to %s, [%s], type %s' % (self.receiver, self.message, self.type)
