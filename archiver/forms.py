from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, FileField, HiddenField


class UploadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    name = StringField("Your name", validators=[DataRequired()])
    files = FileField("File(s)", validators=[FileRequired()])
    password = StringField("Password")


class PasswordForm(FlaskForm):
    password = StringField("Password", validators=[])
    #file_id = HiddenField("File ID")
