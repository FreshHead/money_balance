from money_balance import Gtk
from money_balance.view import NotebookWindow, OperationEntryWindow


class Controller:
    def __init__(self, model):
        self.model = model
        self.tree_view_window = NotebookWindow(model.operation_list_store, model.goal_list_store, model.type_list_store)
        self.entry_window = None
        self.selected_row = None

        self.tree_view_window.connect('operation-insert', self.open_insert_form)
        self.tree_view_window.connect('goal-insert', self.open_update_form)
        self.tree_view_window.connect('type-insert', self.delete_selected_row)
        self.tree_view_window.connect('delete-event', Gtk.main_quit)
        self.tree_view_window.show_all()

    def open_insert_form(self, widget):
        self.entry_window = OperationEntryWindow()
        self.entry_window.connect('save-inserted', self.insert_in_list_store)
        self.entry_window.show_for_insert()

    def open_update_form(self, widget):
        model, self.selected_row = self.tree_view_window.operations_view.get_selection().get_selected()
        if self.selected_row is not None:
            self.entry_window = OperationEntryWindow()
            self.entry_window.connect('save-updated', self.update_in_list_store)
            self.entry_window.show_for_update(model[self.selected_row])

    def delete_selected_row(self, widget):
        model, selected_row = self.tree_view_window.operations_view.get_selection().get_selected()
        self.model.list_store.remove(selected_row)

    def insert_in_list_store(self, widget):
        rows = self.entry_window.get_saving_fields()
        if isinstance(widget, OperationEntryWindow):
            self.model.insert_into_operation(rows)

    def update_in_list_store(self, widget):
        row = self.entry_window.get_saving_fields()
        self.model.list_store[self.selected_row][0] = row[0]
        self.model.list_store[self.selected_row][1] = row[1]
        self.model.list_store[self.selected_row][2] = float(row[2])
