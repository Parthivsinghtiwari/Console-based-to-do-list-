import sqlite3
from tabulate import tabulate
import os

DB_PATH = 'db/tasks.db'
os.makedirs('db', exist_ok=True)

# Initialize DB
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'pending')''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        conn.close()

# Add Task
def add_task(description):
    if not description.strip():
        print("Error: Task description cannot be empty.")
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
        conn.commit()
        print("Task added.")
    except sqlite3.Error as e:
        print(f"Database error while adding task: {e}")
    finally:
        conn.close()

# View Tasks
def view_tasks():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        rows = c.fetchall()
        if rows:
            print(tabulate(rows, headers=['ID', 'Task', 'Status'], tablefmt='grid'))
        else:
            print("No tasks found.")
    except sqlite3.Error as e:
        print(f"Database error while fetching tasks: {e}")
    finally:
        conn.close()

# Mark Task as Done
def mark_done(task_id):
    if not task_id.isdigit():
        print("Error: Task ID must be a number.")
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
        if c.rowcount == 0:
            print(f"No task found with ID {task_id}.")
        else:
            print("Task marked as done.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while marking task done: {e}")
    finally:
        conn.close()

# Delete Task
def delete_task(task_id):
    if not task_id.isdigit():
        print("Error: Task ID must be a number.")
        return
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        if c.rowcount == 0:
            print(f"No task found with ID {task_id}.")
        else:
            print("Task deleted.")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while deleting task: {e}")
    finally:
        conn.close()

# CLI Menu
def menu():
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            desc = input("Enter task description: ").strip()
            add_task(desc)
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            tid = input("Enter task ID to mark as done: ").strip()
            mark_done(tid)
        elif choice == '4':
            tid = input("Enter task ID to delete: ").strip()
            delete_task(tid)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == '__main__':
    init_db()
    menu()
