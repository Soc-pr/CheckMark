# Dependencies
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout


from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from datetime import datetime

# To be added after creating the database
from database import Database

# Initialize db instance
db = Database()


class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%Y %B %d, %A, %H:%M'))

    def on_save(self, instance, value, date_range):
        date = value.strftime('%Y %B %d, %A, %H:%M')
        self.ids.date_text.text = str(date)


# After creating the database.py
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        '''mark the task as selected or unselected'''
        if check.active == True:
            the_list_item.text = '[b]' + the_list_item.text + '[/b]'
            db.mark_task_as_selected(the_list_item.pk)  # here
        else:
            the_list_item.text = str(db.mark_task_as_unselected(the_list_item.pk))  # Here

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)  # Here


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''


# Main App class
class MainApp(MDApp):
    task_list_dialog = None
    all_tasks_list = None

    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

    # Showing the task dialog to add tasks
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def on_start(self):
        # Load the saved tasks and add them to the MDList widget when the application starts
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text='[s]' + task[1] + '[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        '''Add task to the list of tasks'''
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)

        # return the created task details and create a list item
        self.root.ids['container'].add_widget(
            ListItemWithCheckbox(pk=created_task[0], text='[b]' + created_task[1] + '[/b]',
                                 secondary_text=created_task[2]))
        task.text = ''


if __name__ == '__main__':
    app = MainApp()
    app.run()