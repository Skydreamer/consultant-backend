class Task():
    def __init__(self, address, body, type):
        self.address = address
        self.body = body
        self.type = type

    def get_body(self):
        return self.body
       
    def __str__(self):
        return 'From %s, type %s, body %s' % (self.address, self.type, self.body)
