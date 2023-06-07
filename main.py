from datetime import datetime

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from database import Database

db = Database()


class AddingTaskWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%Y %B %d, %A, %H:%M'))

    def on_save(self, instance, value, date_range):
        date = value.strftime('%Y %B %d, %A, %H:%M')
        self.ids.date_text.text = str(date)


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        if check.active:
            the_list_item.text = '[b]' + the_list_item.text + '[/b]'
            db.mark_task_as_selected(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_unselected(the_list_item.pk))

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)  # Here


class ShowCreatedTasks(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_list_widget(self, task, task_date, created_task):
        # created_task = db.create_task(task.text, task_date)
        self.ids.container.add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]' + created_task[1] + '[/b]',
                                                           secondary_text=created_task[2]))
        task.text = ''

    def all_tasks(self):
        selected_task, unselected_task = db.get_tasks()
        if selected_task:
            for task in selected_task:
                add_task = ListItemWithCheckbox(pk=task[0], text='[b]' + task[1] + '[/b]', secondary_text=task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)
        if unselected_task:
            for task in unselected_task:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                self.root.ids.container.add_widget(add_task)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass


class MainApp(MDApp):
    task_list_dialog = None
    all_tasks = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=AddingTaskWindow(),
            )
        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def all_tasks_list(self):
        if not self.all_tasks:
            self.all_tasks = MDDialog(
                title="Your Tasks",
                type="custom",
                content_cls=ShowCreatedTasks()
            )
        self.all_tasks.open()

    def close_tasks(self, *args):
        self.all_tasks.dismiss()

    def create_db_entry(self, task, task_date):
        created_task = db.create_task(task.text, task_date)


if __name__ == '__main__':
    app = MainApp()
    app.run()
