from flask_sqlalchemy import SQLAlchemy  # import database api
from datetime import datetime

db = SQLAlchemy()


class Todo(db.Model):
    """
    class for Todo tasks
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), nullable=False)
    priority = db.Column(db.Integer)
    description = db.Column(db.Text)
    finished = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
