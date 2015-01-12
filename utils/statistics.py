class Statistics:
    req_count = 0
    total_time = 0.0

    @classmethod
    def add_call(cls, time):
        print 'ADD CALL'
        cls.req_count += 1
        cls.total_time += time

    @classmethod
    def avg_time(cls):
        return cls.total_time / cls.req_count

