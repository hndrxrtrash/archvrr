from archiver import db, admin
from flask_admin.contrib.sqla import ModelView


class File(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    file_name = db.Column(db.String(80))
    ext = db.Column(db.String(6))
    title = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(10000))
    size = db.Column(db.Integer())
    created_at = db.Column(db.DateTime())
    key = db.Column(db.String(13))


admin.add_view(ModelView(File, db.session))
