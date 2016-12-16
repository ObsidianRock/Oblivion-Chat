import rethinkdb as r


class DataBase:
    def __init__(self, db):
        self.db = db
        self.conn = r.connect(host='localhost', port=28015, db=self.db)

    def create_table(self, table):
        try:
            r.db(self.db).table_create(table).run(self.conn)
            print('table created')
        except:
            print('table exists')


class Message(DataBase):

    def __init__(self, db, table):
        super().__init__(db)
        self.table = table

    def commit(self, item):
        try:
            r.db(self.db).table(self.table).insert({'message': item}).run(self.conn)
        except Exception as e:
            print(str(e))
            print('couldnt insert items')

