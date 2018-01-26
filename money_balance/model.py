import sqlalchemy as sa
from money_balance import Gtk

class Model:
    def __init__(self):
        self.conn = sa.create_engine("postgresql://postgres:postgres@92.255.198.104:5432/money_balance")

        self.operation_list_store = Gtk.ListStore(int, str, str, str)
        self.populate_operation(self.operation_list_store)


        self.goal_list_store = Gtk.ListStore(int, str, str, str, bool, str)
        self.populate_goal(self.operation_list_store)

        self.type_list_store = Gtk.ListStore(str, int)
        self.populate_type(self.operation_list_store)


    def populate_operation(self, list_store):
        operation_rows = self.conn.execute('SELECT money, type, description, create_date FROM finance.operation')
        for item in operation_rows:
            self.operation_list_store.append([item[0], item[1], item[2], str(item[3])])

    def populate_goal(self, list_store):
        goal_rows = self.conn.execute('SELECT money, type, description, priority, completed, create_date '
                                      'FROM finance.goal')
        for item in goal_rows:
            self.goal_list_store.append([item[0], item[1], item[2], str(item[3]), item[4], str(item[5])])

    def populate_type(self, list_store):
        type_rows = self.conn.execute('SELECT type, default_value FROM finance.type')

        for item in type_rows:
            self.type_list_store.append([item[0], item[1]])

    def insert_into_operation(self, row):
        self.conn.execute("INSERT INTO finance.operation (money, type, description) VALUES("
                          + row[0] + ",'" + row[1] + "','" + row[2] + "')")
