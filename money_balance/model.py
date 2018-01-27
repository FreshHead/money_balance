import sqlalchemy as sa
from money_balance import Gtk


class Model:
    def __init__(self):
        self.conn = sa.create_engine("postgresql://postgres:postgres@92.255.198.104:5432/money_balance")

        self.operation_list_store = Gtk.ListStore(int, int, str, str, str)
        self.populate_operation(self.operation_list_store)

        self.goal_list_store = Gtk.ListStore(int, int, str, str, str, bool, str)
        self.populate_goal(self.goal_list_store)

        self.type_list_store = Gtk.ListStore(str, int)
        self.populate_type(self.type_list_store)

    def populate_operation(self, list_store):
        list_store.clear()
        operation_rows = self.conn.execute('SELECT operation_id, money, type, description, create_date '
                                           'FROM finance.operation')
        for item in operation_rows:
            list_store.append([item[0], item[1], item[2], item[3], str(item[4])])

    def populate_goal(self, list_store):
        list_store.clear()
        goal_rows = self.conn.execute('SELECT goal_id, money, type, description, priority, completed, create_date '
                                      'FROM finance.goal')
        for item in goal_rows:
            list_store.append([item[0], item[1], item[2], item[3], str(item[4]), item[5], str(item[6])])

    def populate_type(self, list_store):
        list_store.clear()
        type_rows = self.conn.execute('SELECT type, default_value FROM finance.type')
        for item in type_rows:
            list_store.append([item[0], item[1]])

    def insert_operation(self, row):
        self.conn.execute("INSERT INTO finance.operation (money, type, description) VALUES("
                          + row[0] + ",'" + row[1] + "','" + row[2] + "')")
        self.populate_operation(self.operation_list_store)

    def update_operation(self, row, id):
        self.conn.execute("UPDATE finance.operation SET money = "
                          + row[0] + " ,type = '"
                          + row[1] + "' ,description = '"
                          + row[2] + "' WHERE operation_id = " + str(id))
        self.populate_operation(self.operation_list_store)

    def delete_operation(self, id):
        self.conn.execute('DELETE FROM finance.operation WHERE operation_id=' + str(id))
        self.populate_operation(self.operation_list_store)

    def insert_goal(self, row):
        self.conn.execute("INSERT INTO finance.goal (money, type, description, priority, completed) VALUES("
                          + row[0] + ",'" + row[1] + "','" + row[2] + "',"+ row[3] + "," + str(row[4]) + ")")
        self.populate_goal(self.goal_list_store)

    def update_goal(self, row, id):
        self.conn.execute("UPDATE finance.goal SET money = " + row[0]
                          + " ,type = '" + row[1]
                          + "' ,description = '" + row[2]
                          + "' ,priority = " + row[3]
                          + ", completed = " + str(row[4])
                          + " WHERE goal_id = " + str(id))
        self.populate_goal(self.goal_list_store)

    def delete_goal(self, id):
        self.conn.execute('DELETE FROM finance.goal WHERE goal_id=' + str(id))
        self.populate_goal(self.goal_list_store)

    def insert_type(self, row):
        if row[1] != '':
            self.conn.execute("INSERT INTO finance.type (type, default_value) VALUES('"
                          + row[0] + "'," + row[1] + ")")
        else:
            self.conn.execute("INSERT INTO finance.type (type) VALUES('"
                              + row[0] + "')")
        self.populate_type(self.type_list_store)

    def update_type(self, row, type):
        self.conn.execute("UPDATE finance.type SET type = '" + row[0]
                          + "', default_value = " + row[1]
                          + " WHERE type = '" + type + "'")
        self.populate_type(self.type_list_store)

    def delete_type(self, type):
        self.conn.execute("DELETE FROM finance.type WHERE type='" + type + "'")
        self.populate_type(self.type_list_store)

