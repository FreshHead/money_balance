from money_balance import Gtk, GObject


def create_tree_view(list_store, columns_list):
    view = Gtk.TreeView(list_store)
    view.set_size_request(650, 400)

    for i, col_title in enumerate(columns_list):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(col_title, renderer, text=i)
        if column.get_title() == 'id':
            column.set_visible(False)
        column.set_sort_column_id(i)  # Make column sortable and selectable
        view.append_column(column)
    return view


class NotebookWindow(Gtk.Window):
    __gsignals__ = {
        'operation-insert': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'operation-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'operation-delete': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'goal-insert': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'goal-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'goal-delete': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'type-insert': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'type-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'type-delete': (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def __init__(self, operation_list_store, goal_list_store, type_list_store):
        super().__init__(title="Денежный баланс")
        super().set_resizable(False)

        vbox = Gtk.VBox()
        self.add(vbox)

        hbox = Gtk.HBox()
        vbox.add(hbox)

        insert_button = Gtk.Button("Добавить")
        hbox.add(insert_button)
        insert_button.connect("clicked", self.on_insert)

        update_button = Gtk.Button("Изменить")
        hbox.add(update_button)
        update_button.connect("clicked", self.on_update)

        delete_button = Gtk.Button("Удалить")
        hbox.add(delete_button)
        delete_button.connect("clicked", self.on_delete)

        self.notebook = Gtk.Notebook()
        vbox.add(self.notebook)

        self.operation_page = Gtk.Box()
        self.operation_view = create_tree_view(operation_list_store, ["id", "Сумма", "Тип", "Описание", "Дата создания"])
        self.operation_page.add(self.operation_view)
        self.notebook.append_page(self.operation_page, Gtk.Label("Зарплаты/Траты"))

        goal_page = Gtk.Box()
        self.goal_view = create_tree_view(goal_list_store, ["id", "Сумма", "Тип", "Описание",
                                                            "Приоритет", "Выполнено", "Дата создания"])
        goal_page.add(self.goal_view)
        self.notebook.append_page(goal_page, Gtk.Label("Цели"))

        type_page = Gtk.Box()
        self.type_view = create_tree_view(type_list_store, ["Тип", "Цена по умолчанию"])
        type_page.add(self.type_view)
        self.notebook.append_page(type_page, Gtk.Label("Типы"))

    def on_insert(self, widget):
        current_page_index = self.notebook.get_current_page()
        if current_page_index == 0:
            self.emit("operation-insert")
        elif current_page_index == 1:
            self.emit('goal-insert')
        elif current_page_index == 2:
            self.emit('type-insert')

    def on_update(self, widget):
        current_page_index = self.notebook.get_current_page()
        if current_page_index == 0:
            self.emit("operation-update")
        elif current_page_index == 1:
            self.emit('goal-update')
        elif current_page_index == 2:
            self.emit('type-update')

    def on_delete(self, widget):
        current_page_index = self.notebook.get_current_page()
        if current_page_index == 0:
            self.emit("operation-delete")
        elif current_page_index == 1:
            self.emit('goal-delete')
        elif current_page_index == 2:
            self.emit('type-delete')


class OperationEntryWindow(Gtk.Window):
    __gsignals__ = {
        'save-inserted': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'save-updated': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(layout)

        money_box = Gtk.Box()
        layout.add(money_box)
        money_label = Gtk.Label("Сумма:")
        self.money_entry = Gtk.Entry()

        money_box.pack_start(money_label, False, False, 0)
        money_box.pack_end(self.money_entry, False, False, 0)

        type_box = Gtk.Box()
        layout.add(type_box)
        type_label = Gtk.Label("Тип:")
        self.type_entry = Gtk.Entry()

        type_box.pack_start(type_label, False, False, 0)
        type_box.pack_end(self.type_entry, False, False, 0)

        description_box = Gtk.Box()
        layout.add(description_box)
        description_label = Gtk.Label("Описание:")
        self.description_entry = Gtk.Entry()

        description_box.pack_start(description_label, False, False, 0)
        description_box.pack_end(self.description_entry, False, False, 0)

        button_box = Gtk.HButtonBox()
        layout.add(button_box)
        self.save = Gtk.Button(stock=Gtk.STOCK_OK)
        self.cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)

        button_box.add(self.save)
        button_box.add(self.cancel)

        self.cancel.connect("clicked", self.on_cancel)

    def on_cancel(self, widget):
        self.close()

    def show_for_insert(self):
        self.set_title('Добавление зарплаты/расхода')
        self.save.connect("clicked", self.on_insert_clicked)
        self.show_all()

    def show_for_update(self, row):
        self.set_title('Редактирование зарплаты/расхода')
        self.money_entry.set_text(str(row[1]))
        self.type_entry.set_text(row[2])
        self.description_entry.set_text(str(row[3]))
        self.save.connect("clicked", self.on_update_clicked)
        self.show_all()

    def get_saving_fields(self):
        return [self.money_entry.get_text(), self.type_entry.get_text(), self.description_entry.get_text()]

    def on_insert_clicked(self, widget):
        if self.is_ready_for_save():
            self.emit('save-inserted')
            self.close()

    def on_update_clicked(self, widget):
        if self.is_ready_for_save():
            self.emit('save-updated')
            self.close()

    def is_ready_for_save(self):
        return self.money_entry.get_text() != '' and self.type_entry.get_text() != ''


class GoalEntryWindow(Gtk.Window):
    __gsignals__ = {
        'save-inserted': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'save-updated': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(layout)

        money_box = Gtk.Box()
        layout.add(money_box)
        money_label = Gtk.Label("Сумма:")
        self.money_entry = Gtk.Entry()

        money_box.pack_start(money_label, False, False, 0)
        money_box.pack_end(self.money_entry, False, False, 0)

        type_box = Gtk.Box()
        layout.add(type_box)
        type_label = Gtk.Label("Тип:")
        self.type_entry = Gtk.Entry()

        type_box.pack_start(type_label, False, False, 0)
        type_box.pack_end(self.type_entry, False, False, 0)

        description_box = Gtk.Box()
        layout.add(description_box)
        description_label = Gtk.Label("Описание:")
        self.description_entry = Gtk.Entry()

        description_box.pack_start(description_label, False, False, 0)
        description_box.pack_end(self.description_entry, False, False, 0)

        priority_box = Gtk.Box()
        layout.add(priority_box)
        priority_label = Gtk.Label("Приоритет:")
        self.priority_entry = Gtk.Entry()

        priority_box.pack_start(priority_label, False, False, 0)
        priority_box.pack_end(self.priority_entry, False, False, 0)

        completed_box = Gtk.Box()
        layout.add(completed_box)
        completed_label = Gtk.Label("Выполнено:")
        self.completed_checkButton = Gtk.CheckButton()

        completed_box.pack_start(completed_label, False, False, 0)
        completed_box.pack_end(self.completed_checkButton, False, False, 0)

        button_box = Gtk.HButtonBox()
        layout.add(button_box)
        self.save = Gtk.Button(stock=Gtk.STOCK_OK)
        self.cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)

        button_box.add(self.save)
        button_box.add(self.cancel)

        self.cancel.connect("clicked", self.on_cancel)

    def on_cancel(self, widget):
        self.close()

    def show_for_insert(self):
        self.set_title('Добавление целей')
        self.save.connect("clicked", self.on_insert_clicked)
        self.show_all()

    def show_for_update(self, row):
        self.set_title('Редактирование целей')
        self.money_entry.set_text(str(row[1]))
        self.type_entry.set_text(row[2])
        self.description_entry.set_text(str(row[3]))
        self.priority_entry.set_text(row[4])
        self.completed_checkButton.set_active(row[5])

        self.save.connect("clicked", self.on_update_clicked)
        self.show_all()

    def get_saving_fields(self):
        return [self.money_entry.get_text(), self.type_entry.get_text(), self.description_entry.get_text(),
                self.priority_entry.get_text(), self.completed_checkButton.get_active()]

    def on_insert_clicked(self, widget):
        if self.is_ready_for_save():
            self.emit('save-inserted')
            self.close()

    def on_update_clicked(self, widget):
        if self.is_ready_for_save():
            self.emit('save-updated')
            self.close()

    def is_ready_for_save(self):
        return self.money_entry.get_text() != '' and self.type_entry.get_text() != '' and self.priority_entry.get_text() != ''


class TypeEntryWindow(Gtk.Window):
    __gsignals__ = {
        'save-inserted': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'save-updated': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def __init__(self):
        super().__init__()
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(layout)

        type_box = Gtk.Box()
        layout.add(type_box)
        type_label = Gtk.Label("Тип:")
        self.type_entry = Gtk.Entry()

        type_box.pack_start(type_label, False, False, 0)
        type_box.pack_end(self.type_entry, False, False, 0)

        default_value_box = Gtk.Box()
        layout.add(default_value_box)
        default_value_label = Gtk.Label("Значение по умолчанию:")
        self.default_value_entry = Gtk.Entry()

        default_value_box.pack_start(default_value_label, False, False, 0)
        default_value_box.pack_end(self.default_value_entry, False, False, 0)

        button_box = Gtk.HButtonBox()
        layout.add(button_box)
        self.save = Gtk.Button(stock=Gtk.STOCK_OK)
        self.cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)

        button_box.add(self.save)
        button_box.add(self.cancel)

        self.cancel.connect("clicked", self.on_cancel)

    def on_cancel(self, widget):
        self.close()

    def show_for_insert(self):
        self.set_title('Добавление цели')
        self.save.connect("clicked", self.on_insert_clicked)
        self.show_all()

    def show_for_update(self, row):
        self.set_title('Редактирование цели')
        self.type_entry.set_text(row[0])
        self.default_value_entry.set_text(str(row[1]))
        self.save.connect("clicked", self.on_update_clicked)
        self.show_all()

    def get_saving_fields(self):
        return [self.type_entry.get_text(), self.default_value_entry.get_text()]

    def on_insert_clicked(self, widget):
        if self.is_ready_for_save():
            self.emit('save-inserted')
            self.close()

    def on_update_clicked(self, widget):
        if self.is_ready_for_save():
            self.emit('save-updated')
            self.close()

    def is_ready_for_save(self):
        return self.type_entry.get_text() != ''
