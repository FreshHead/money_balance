from money_balance import Gtk
from money_balance.view import NotebookWindow, OperationEntryWindow, GoalEntryWindow, TypeEntryWindow


class Controller:
    def __init__(self, model):
        self.model = model
        self.notebook_window = NotebookWindow(model.operation_list_store, model.goal_list_store, model.type_list_store)
        self.entry_window = None
        self.selected_row = None

        self.notebook_window.connect('operation-insert', self.open_insert_operation_form)
        self.notebook_window.connect('operation-update', self.open_update_operation_form)
        self.notebook_window.connect('operation-delete', self.delete_selected_operation_row)

        self.notebook_window.connect('goal-insert', self.open_insert_goal_form)
        self.notebook_window.connect('goal-update', self.open_update_goal_form)
        self.notebook_window.connect('goal-delete', self.delete_selected_goal_row)

        self.notebook_window.connect('type-insert', self.open_insert_type_form)
        self.notebook_window.connect('type-update', self.open_update_type_form)
        self.notebook_window.connect('type-delete', self.delete_selected_type_row)

        self.notebook_window.connect('delete-event', Gtk.main_quit)
        self.notebook_window.show_all()

    def open_insert_operation_form(self, widget):
        self.entry_window = OperationEntryWindow()
        self.entry_window.connect('save-inserted', self.insert_in_list_store)
        self.entry_window.show_for_insert()

    def open_update_operation_form(self, widget):
        model, self.selected_row = self.notebook_window.operation_view.get_selection().get_selected()
        if self.selected_row is not None:
            self.entry_window = OperationEntryWindow()
            self.entry_window.connect('save-updated', self.update_in_list_store)
            self.entry_window.show_for_update(model[self.selected_row])

    def delete_selected_operation_row(self, widget):
        (model, pathlist) = self.notebook_window.operation_view.get_selection().get_selected_rows()
        tree_iter = model.get_iter(pathlist[0])
        id = model.get_value(tree_iter, 0)
        self.model.delete_operation(id)

    def open_insert_goal_form(self, widget):
        self.entry_window = GoalEntryWindow()
        self.entry_window.connect('save-inserted', self.insert_in_list_store)
        self.entry_window.show_for_insert()

    def open_update_goal_form(self, widget):
        model, self.selected_row = self.notebook_window.goal_view.get_selection().get_selected()
        if self.selected_row is not None:
            self.entry_window = GoalEntryWindow()
            self.entry_window.connect('save-updated', self.update_in_list_store)
            self.entry_window.show_for_update(model[self.selected_row])

    def delete_selected_goal_row(self, widget):
        (model, pathlist) = self.notebook_window.goal_view.get_selection().get_selected_rows()
        tree_iter = model.get_iter(pathlist[0])
        id = model.get_value(tree_iter, 0)
        self.model.delete_goal(id)

    def open_insert_type_form(self, widget):
        self.entry_window = TypeEntryWindow()
        self.entry_window.connect('save-inserted', self.insert_in_list_store)
        self.entry_window.show_for_insert()

    def open_update_type_form(self, widget):
        model, self.selected_row = self.notebook_window.type_view.get_selection().get_selected()
        if self.selected_row is not None:
            self.entry_window = TypeEntryWindow()
            self.entry_window.connect('save-updated', self.update_in_list_store)
            self.entry_window.show_for_update(model[self.selected_row])

    def delete_selected_type_row(self, widget):
        (model, pathlist) = self.notebook_window.type_view.get_selection().get_selected_rows()
        tree_iter = model.get_iter(pathlist[0])
        id = model.get_value(tree_iter, 0)
        self.model.delete_type(id)

    def insert_in_list_store(self, widget):
        rows = self.entry_window.get_saving_fields()
        if isinstance(widget, OperationEntryWindow):
            self.model.insert_operation(rows)
        elif isinstance(widget, GoalEntryWindow):
            self.model.insert_goal(rows)
        elif isinstance(widget, TypeEntryWindow):
            self.model.insert_type(rows)

    def update_in_list_store(self, widget):
        row = self.entry_window.get_saving_fields()
        if isinstance(widget, OperationEntryWindow):
            (model, pathlist) = self.notebook_window.operation_view.get_selection().get_selected_rows()
            tree_iter = model.get_iter(pathlist[0])
            id = model.get_value(tree_iter, 0)
            self.model.update_operation(row, id)
        elif isinstance(widget, GoalEntryWindow):
            (model, pathlist) = self.notebook_window.goal_view.get_selection().get_selected_rows()
            tree_iter = model.get_iter(pathlist[0])
            id = model.get_value(tree_iter, 0)
            self.model.update_goal(row, id)
        elif isinstance(widget, TypeEntryWindow):
            (model, pathlist) = self.notebook_window.type_view.get_selection().get_selected_rows()
            tree_iter = model.get_iter(pathlist[0])
            id = model.get_value(tree_iter, 0)
            self.model.update_type(row, id)



