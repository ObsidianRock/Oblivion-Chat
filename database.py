import rethinkdb as r


class Message:

    def __init__(self):

        self.db = 'Chat'
        self.table = 'messages'

        try:
            self.conn = r.connect(host='localhost', port=28015, db=self.db)
            print('Connected')
        except:
            self.conn = None
            print('Cant connect')

    def commit(self, item):
        print(item)
        try:
            r.db(self.db).table(self.table).insert({'message': item}).run(self.conn)
        except Exception as e:
            print(str(e))
            print('couldnt insert items')

    def create_table(self):
        try:
            r.db(self.db).table_create(self.table).run(self.conn)
        except:
            print('table exists')