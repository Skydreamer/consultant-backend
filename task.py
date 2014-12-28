class Task():
    def __init__(self, body, type):
        self.body = body
        self.type = type

    def get_body(self):
        return self.body
       
    def __str__(self):
        return str(self.body)
