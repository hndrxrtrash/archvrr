from flask import render_template, send_from_directory, redirect, url_for, current_app, request
from werkzeug.exceptions import RequestEntityTooLarge
from archiver.forms import UploadForm, PasswordForm
from archiver import app, db, bcrypt
from archiver.models import File
from sqlalchemy import func
from random import randint
import datetime
import zipfile
import os


@app.errorhandler(413)
def file_is_too_large(e):
    return redirect('/?error=413'), 413


@app.route('/', methods=['POST', "GET"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        new_file = File()
        title, name = form.title.data, form.name.data
        if len(form.files.raw_data) > 1:
            file_names = []
            key = random_string()
            zipf = zipfile.ZipFile('media/ready/'+key + '.zip', 'w', zipfile.ZIP_DEFLATED)
            new_file.ext = "zip"
            files_raw_data = form.files.raw_data
            for file_source in files_raw_data:
                file_name_ = random_string()
                file_name = file_name_+'.'+file_source.filename.split('.')[-1]
                file_source.save("media/files/"+file_name)
                file_names.append(file_name)
                zipf.write('media/files/'+file_name, arcname=file_source.filename)
            zipf.close()
            for file_name in file_names:
                os.remove("media/files/"+file_name)
            new_file.title, new_file.name = title, name
            new_file.file_name = key
        else:
            new_file.title, new_file.name = title, name
            new_file.file_name = random_string()
            new_file.ext = form.files.raw_data[0].filename.split('.')[-1]
            form.files.raw_data[0].save('media/ready/'+new_file.file_name+'.'+new_file.ext)
        new_file.created_at = datetime.datetime.now()
        new_file.size = os.path.getsize("media/ready/"+new_file.file_name+"."+new_file.ext)
        new_file.key = random_string()[:6]
        if form.password.data != "":
            password_hash = bcrypt.generate_password_hash(form.password.data)
            new_file.password_hash = password_hash
        else:
            new_file.password_hash = ""
        db.session.add(new_file)
        db.session.commit()
        number = File.query.filter_by(title=new_file.title).count()
        new_filename = new_file.title.replace(" ", "-") + "-" + str(number)
        return redirect(url_for('file_view', title=new_filename))
    if request.args.get('error') == "413":
        return render_template("index.html", form=form,
                               error="Your file is too large. File size should be no more than 500MB")
    return render_template("index.html", form=form)


@app.route('/f/<title>/', methods=["GET", "POST"])
def file_view(title):
    number = int(title.split('-')[-1])
    title_1 = title.replace(str(number), "").replace('-', ' ')
    title_1 = title_1[:len(title_1)-1]
    try: file_obj = File.query.filter(func.lower(File.title) == func.lower(title_1)).all()[number-1]
    except IndexError: return redirect('/')
    if file_obj.ext == "zip":
        zip_file = zipfile.ZipFile('media/ready/'+file_obj.file_name+'.zip', 'r')
        file_list = zip_file.namelist()
    else: file_list = None
    file_size = human_readable_size(file_obj.size)
    form = PasswordForm()
    if form.validate_on_submit():
        if file_obj.password_hash == "":
            return send_from_directory("../media", 'ready/' + file_obj.file_name + '.' + file_obj.ext,
                                       as_attachment=True, attachment_filename=file_obj.title+'.'+file_obj.ext)
        if bcrypt.check_password_hash(file_obj.password_hash, form.password.data):
            return send_from_directory('../media', 'ready/' + file_obj.file_name + '.' + file_obj.ext,
                                       as_attachment=True, attachment_filename=file_obj.title+'.'+file_obj.ext)
        else:
            return render_template('file.html', file=file_obj, files=file_list,
                                    password_form=form, size=file_size,
                                    error="Password is incorrect", short=True)
    return render_template('file.html', file=file_obj, files=file_list,
                                    password_form=form, size=file_size, short=True)


@app.route("/<key>/")
def short(key):
    file_obj = File.query.filter_by(key=key).first()
    if file_obj.ext == "zip":
        zip_file = zipfile.ZipFile('media/ready/'+file_obj.file_name+'.zip', 'r')
        file_list = zip_file.namelist()
    else: file_list = None
    file_size = human_readable_size(file_obj.size)
    form = PasswordForm()
    if form.validate_on_submit():
        if file_obj.password_hash == "":
            return send_from_directory("../media", 'ready/' + file_obj.file_name + '.' + file_obj.ext,
                                       as_attachment=True, attachment_filename=file_obj.title+'.'+file_obj.ext)
        if bcrypt.check_password_hash(file_obj.password_hash, form.password.data):
            return send_from_directory('../media', 'ready/' + file_obj.file_name + '.' + file_obj.ext,
                                       as_attachment=True, attachment_filename=file_obj.title+'.'+file_obj.ext)
        else:
            return render_template('file.html', file=file_obj, files=file_list,
                                    password_form=form, size=file_size,
                                    link=get_long_link(file_obj),
                                    error="Password is incorrect", short=False)
    return render_template('file.html', file=file_obj, files=file_list,
                                    password_form=form, size=file_size, short=False,
                                    link=get_long_link(file_obj))



def random_string():
    chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    string = ""
    for i in range(10):
        string += chars[randint(0, len(chars)-1)]
    return string

def human_readable_size(memory):
    if memory > 1024 * 1024 * 1024:
        string = "{0:.2f}GB".format(memory / (1024 * 1024 * 1024))
    elif memory > 1024 * 1024:
        string = "{0:.2f}MB".format(memory / (1024 * 1024))
    elif memory > 1024:
        string = "{0:.2f}KB".format(memory / 1024)
    else:
        string = "0GB"
    return string

def get_long_link(fileObj):
    for i, f in enumerate(File.query.filter_by(title=fileObj.title).all()):
        if f.id == fileObj.id:
            break
    return title.replace(" ", "-") + "-" + str(i+1)
