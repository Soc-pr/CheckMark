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
        self.cursor.execute("INSERT INTO tasks(task, time_date, selected) "
                            "VALUES(?,?,?)", (task, time_date, 0))
        self.con.commit()

        created_task = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE task = ?"
                                           "and selected = 0", (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        print("veikia db get_tasks")
        unselected_tasks = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected = 0").fetchall()
        selected_task = self.cursor.execute("SELECT id, task, time_date FROM tasks WHERE selected= 1").fetchall()
        # print(unselected_tasks)
        return selected_task, unselected_tasks

    def mark_task_as_selected(self, taskid):
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