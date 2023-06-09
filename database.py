import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect("check.db")
        self.cursor = self.con.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT, "
                            "task varchar(20) NOT NULL, time_date varchar(50), "
                            "selected BOOLEAN NOT NULL CHECK (selected IN (0,1)))")
        self.con.commit()

    def create_task(self, task, time_date=None):
        self.cursor.execute("UPDATE tasks SET selected = 0")
        self.cursor.execute("INSERT INTO tasks(task, time_date, selected) "
                            "VALUES(?,?,?)", (task, time_date, 1))
        self.con.commit()

        created_task = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE task = ?"
                                           "and selected = 1", (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        unselected_tasks = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected = 0").fetchall()
        selected_task = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected= 1").fetchall()
        return selected_task, unselected_tasks

    def get_selected_task(self):
        selected_task = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected = 1").fetchall()
        return selected_task

    def push_the_big(self, time_date=None):
        selected_task = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected= 1").fetchall()
        self.cursor.execute("INSERT INTO tasks(task, time_date, selected) "
                            "VALUES(?,?,?)", (selected_task[0][1], time_date, 1))
        self.con.commit()

    def get_selected_list(self):
        selected_list_ = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected = 1").fetchall()
        task_name = selected_list_[0][1]
        query = f"SELECT id, task, time_date FROM tasks WHERE task = '{task_name}' ORDER BY id DESC"
        selected_list = self.cursor.execute(query).fetchall()
        return selected_list

    def mark_task_as_selected(self, taskid):
        self.cursor.execute("UPDATE tasks SET selected = 0")
        self.cursor.execute("UPDATE tasks SET selected = 1 WHERE id = ?", (taskid,))
        self.con.commit()

    # def crate_new_selected_instance(self, task, time_date=None):
    #     self.cursor.execute("INSERT INTO tasks(task, time_date, selected) VALUES(?,?,?)", (task, time_date, 1))
    #     self.con.commit()

    def mark_task_as_unselected(self, taskid):
        self.cursor.execute("UPDATE tasks SET selected = 0 WHERE id = ?", (taskid,))
        self.con.commit()

        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text[0][0]

    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()
