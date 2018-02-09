from archiver import db, admin
from flask_admin.contrib.sqla import ModelView


class File(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    file_name = db.Column(db.String(80))
    file_format = db.Column(db.String(6))
    title = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime())


admin.add_view(ModelView(File, db.session))
