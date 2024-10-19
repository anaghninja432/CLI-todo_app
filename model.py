import os
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy


class Todo:
    def __init__(self,task,category,date_added=None,date_completed=None,status=None,position=None):
        self.task=task
        self.category=category
        self.date_added=date_added if date_added else datetime.now().isoformat()
        self.date_completed=date_completed if date_completed else None
        self.status=status if status else 1
        self.position=position if position else None

    def __repr__(self) -> str:
        return f"{self.task}, {self.category}, {self.date_added}, {self.date_completed}, {self.status}, {self.position}"

