import sqlite3
from typing import List, Tuple
import datetime
from model import Todo

conn=sqlite3.connect('todo.db')
c=conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                (task TEXT, category TEXT, date_added TEXT, date_completed TEXT, status INTEGER, position INTEGER)''')

create_table()

def insert_todo(todo: Todo):
    c.execute('Select count(*) from todos')
    count=c.fetchone()[0]
    todo.position=count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (?,?,?,?,?,?)',(todo.task,todo.category,todo.date_added,todo.date_completed,todo.status,todo.position))

def get_all_todos():
    c.execute('SELECT * FROM todos')
    results= c.fetchall()
    todos=[]
    for row in results:
        todos.append(Todo(row[0],row[1],row[2],row[3],row[4],row[5]))

    return todos

def delete_todo(position: int):
    c.execute('Select count(*) from todos')
    count=c.fetchone()[0]
    with conn:
        c.execute('DELETE FROM todos WHERE position=?',(position,))
        for pos in range(position+1,count):
            # c.execute('UPDATE todos SET position=? WHERE position=?',(i-1,i))
            change_position(pos,pos-1,False)

# def update_todo(position: int, task: str, category: str):
#     c.execute('UPDATE todos SET task=?, category=? WHERE position=?',(task,category,position))
#     if task:
#         conn.commit()

def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE todos SET position=? WHERE position=?',(new_position,old_position))
    if commit:
        conn.commit()

def update_todo(position: int, task: str, category: str):
    with conn:
        if task and category :
            c.execute('UPDATE todos SET task=?, category=? WHERE position=?',(task,category,position))
        elif task:
            c.execute('UPDATE todos SET task = ? WHERE position = ?',(task,position))
        elif category:
            c.execute('UPDATE todos SET category = ? WHERE position = ?',(category,position))
def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status=2, date_completed=:date_completed WHERE position=:position',{'position':position,'date_completed':datetime.datetime.now().isoformat()})