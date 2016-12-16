

class Connection:
    def __init__(self):
        self.conn = 0

    def new_connection(self):
        self.conn += 1

    def left_conn(self):
        self.conn += -1

    def num_conn(self):
        return self.conn
