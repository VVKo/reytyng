# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask import json
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from datetime import date

import config as config
from helper import *

__author__ = 'VVKo'

reytyng = Flask(__name__, template_folder='templates')
reytyng.config.from_object(config)

# ensure responses aren't cached
if reytyng.config["DEBUG"]:
    @reytyng.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
reytyng.config["SESSION_FILE_DIR"] = mkdtemp()
reytyng.config["SESSION_PERMANENT"] = False
reytyng.config["SESSION_TYPE"] = "filesystem"
Session(reytyng)

db = SQLAlchemy(reytyng)


@reytyng.route('/', methods=['GET', 'POST'])
@login_required
def index():
    '''
    Основна сторінка
    '''
    if request.method == 'POST':
        form = ModuleForm(request.form)

        if form.validate():
            # так как до первого коммита мы не знаем ID статьи, то сначала коммитим с тем, что
            # в шаблоне по умолчанию 'new', а потом в url подставляем id статьи и коммити еще раз
            module = Module(**form.data)
            db.session.add(module)
            db.session.commit()

            module.module_url = str(module.id)
            db.session.commit()

            return redirect(url_for('index'))
        else:
            return render_template('errors.html', errors_text=str(form.errors))

    all_modules = Module.query.all()

    return render_template('index.html', modules=all_modules, date_today=date.today())


@reytyng.route('/modules', methods=['GET', 'POST'])
@login_required
def modules():
    all_modules = Module.query.all()

    return render_template('modules.html', modules=enumerate(all_modules, 1))


@reytyng.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    return render_template('students.html')


@reytyng.route('/kurators', methods=['GET', 'POST'])
@login_required
def kurators():
    return render_template('kurators.html')


@reytyng.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    return render_template('groups.html')



@reytyng.route('/shopping', methods=['GET', 'POST'])
@login_required
def shopping():
    return render_template('shopping.html')


@reytyng.route('/add/module', methods=['POST'])
@login_required
def add_module():
    print('=================')
    form = ModuleForm(request.form)

    print('form=', form.data)

    if form.validate():
        module = Module(**form.data)
        db.session.add(module)
        db.session.commit()

        module.module_url = str(module.id)
        db.session.commit()

        return jsonify({'success': True})
    else:
        return render_template('errors.html', errors_text=str(form.errors))


@reytyng.route('/students/get/all')
@login_required
def get_all_students():
    all_students = Student.query.all()
    return json.dumps([i.serialize for i in all_students])


@reytyng.route('/kurators/get/all')
@login_required
def get_all_kurators():
    all_kurators = Kurator.query.all()
    return json.dumps([i.serialize for i in all_kurators])


@reytyng.route('/groups/get/all')
@login_required
def get_all_groups():
    all_groups = Grupa.query.all()
    return json.dumps([i.serialize for i in all_groups])


@reytyng.route('/student/<int:stud_id>', methods=['GET', 'POST'])
@login_required
def card_student(stud_id):
    stud = Student.query.filter_by(id=stud_id).first()
    return render_template('student.html', student=stud)


@reytyng.route('/add/student', methods=['POST'])
@login_required
def add_student():
    form = StudentForm(request.form)
    print("sudent =", form.data)
    if form.validate():
        student = Student(**form.data)
        db.session.add(student)
        db.session.commit()

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/add/kurator', methods=['POST'])
@login_required
def add_kurator():
    form = KuratorForm(request.form)
    if form.validate():
        kurator = Kurator(**form.data)
        db.session.add(kurator)
        db.session.commit()

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/add/group', methods=['POST'])
@login_required
def add_group():
    form = GrupaForm(request.form)
    if form.validate():
        group = Grupa(**form.data)
        db.session.add(group)
        db.session.commit()

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/add/task', methods=['POST'])
@login_required
def add_task():
    print('=================')
    form = TaskForm(request.form)

    print('form=', form.data)

    if form.validate():
        task = Task(**form.data)
        db.session.add(task)
        db.session.commit()

        task.task_url = str(task.id)
        db.session.commit()

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/add/answer/choice', methods=['POST'])
@login_required
def add_answer_choice():
    form = AnswerChoiceForm(request.form)

    if form.validate():
        answer = AnswerChoice(**form.data)
        db.session.add(answer)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/add/answer/match', methods=['POST'])
@login_required
def add_answer_match():
    form = AnswerMatchForm(request.form)

    if form.validate():
        answer = AnswerMatch(**form.data)
        db.session.add(answer)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/tasks/<task_url>/delete/', methods=['POST', 'GET'])
@login_required
def delete_task(task_url):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_url).first()
        db.session.delete(task)
        db.session.commit()
        AnswerMatch.query.filter_by(task_id=task_url).delete()
        db.session.commit()
        AnswerChoice.query.filter_by(task_id=task_url).delete()

        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


@reytyng.route('/answer/match/<int:answer_id>/delete/', methods=['POST', 'GET'])
@login_required
def delete_answer_match(answer_id):
    if request.method == 'POST':
        r = AnswerMatch.query.filter_by(id=answer_id).first()
        db.session.delete(r)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


@reytyng.route('/answer/choice/<int:answer_id>/delete/', methods=['POST', 'GET'])
@login_required
def delete_answer_choice(answer_id):
    if request.method == 'POST':
        r = AnswerChoice.query.filter_by(id=answer_id).first()
        db.session.delete(r)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


@reytyng.route('/answer/choice/<int:answer_id>/get/')
@login_required
def get_answer_choice(answer_id):
    r = AnswerChoice.query.filter_by(id=answer_id).first()
    # return json.dumps(r.serialize)
    if r:
        return jsonify(answer=r.serialize)
    else:
        return None


@reytyng.route('/answer/choice/<int:answer_id>/update/', methods=['POST'])
@login_required
def update_answer_choice(answer_id):
    form = AnswerChoiceForm(request.form)

    if form.validate():
        d = form.data
        d.pop('task_id')
        AnswerChoice.query.filter_by(id=answer_id).update(d)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/task/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    form = TaskForm(request.form)
    print('form=', form.data)

    if form.validate():
        d = form.data

        d.pop('task_url')
        print('d=', d)
        Task.query.filter_by(id=task_id).update(d)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/answer/match/<int:answer_id>/update/', methods=['POST'])
@login_required
def update_answer_match(answer_id):
    form = AnswerMatchForm(request.form)

    if form.validate():
        d = form.data
        d.pop('task_id')

        AnswerMatch.query.filter_by(id=answer_id).update(d)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@reytyng.route('/answer/match/<int:answer_id>/get/')
@login_required
def get_answer_match(answer_id):
    r = AnswerMatch.query.filter_by(id=answer_id).first()
    # return json.dumps(r.serialize)
    if r:
        return jsonify(answer=r.serialize)
    else:
        return None


@reytyng.route('/task/<task_url>/get')
@login_required
def get_task(task_url):
    task = Task.query.filter_by(task_url=task_url).first()
    if task:
        return jsonify(task=task.serialize)
    return None


@reytyng.route('/getModules')
@login_required
def get_modules():
    all_modules = Module.query.all()
    return json.dumps([i.serialize for i in all_modules])


@reytyng.route('/get/module/<module_url>')
@login_required
def get_tasks(module_url):
    module = Module.query.filter_by(module_url=module_url).first()
    all_tasks = Task.query.filter_by(module=module)
    return json.dumps([i.serialize for i in all_tasks])


@reytyng.route('/module/<module_url>', methods=['GET', 'POST'])
@login_required
def new_task(module_url):
    form = TaskForm(request.form)
    module = Module.query.filter_by(module_url=module_url).first()
    if request.method == 'POST':

        if form.validate():
            task = Task(**form.data)
            db.session.add(task)
            db.session.commit()

            task.task_url = str(task.id)
            db.session.commit()
        else:
            return render_template('errors.html', errors_text=str(form.errors))

    all_tasks = Task.query.filter_by(module=module)

    return render_template('task.html', tasks=all_tasks, module=module)


@reytyng.route('/get/module/<module_url>/<task_url>', methods=['GET', 'POST'])
@login_required
def get_question(module_url, task_url):
    task = Task.query.filter_by(task_url=task_url).first()
    module = Module.query.filter_by(module_url=module_url).first()
    if task.answer_type == 'choice':
        all_answers = AnswerChoice.query.filter_by(task=task)
    else:
        all_answers = AnswerMatch.query.filter_by(task=task)
    return json.dumps([i.serialize for i in all_answers])


@reytyng.route('/module/<module_url>/<task_url>', methods=['GET', 'POST'])
@login_required
def new_question(module_url, task_url):
    task = Task.query.filter_by(task_url=task_url).first()
    module = Module.query.filter_by(module_url=module_url).first()

    print("task_answer_type =", task.answer_type)

    if task.answer_type == 'choice':
        form = AnswerChoiceForm(request.form)
    else:
        form = AnswerMatchForm(request.form)

    if request.method == 'POST':
        if form.validate():

            if task.answer_type == 'choice':
                answer = AnswerChoice(**form.data)
            else:
                answer = AnswerMatch(**form.data)

            db.session.add(answer)
            db.session.commit()
        else:
            return render_template('errors.html', errors_text=str(form.errors))

    if task.answer_type == 'choice':
        all_answers = AnswerChoice.query.filter_by(task=task)
    else:
        all_answers = AnswerMatch.query.filter_by(task=task)

    return render_template('answer.html', answers=all_answers, task=task, module=module)


@reytyng.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    users = Users.query.all()
    form = UsersForm(request.form)

    if len(users) == 0:
        return redirect(url_for("register"))

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("username"):
            return "must provide username"

            # ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"

        rows = Users.query.filter_by(username=request.form.get("username")).first()

        # ensure username exists and password is correct
        if type(rows) == 'NoneType' or not pwd_context.verify(request.form.get("password"), rows.hash):
            return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = rows.id

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@reytyng.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@reytyng.route("/register", methods=["POST", "GET"])
def register():
    """Log user in."""

    # forget any user_id
    session.clear()
    form = UsersForm(request.form)

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if form.validate():
            user = Users(**form.data)
            print('user_pass', request.form.get('password'))
            user.hash = pwd_context.hash(request.form.get('password'))
            db.session.add(user)
            print('user_pass', user.hash)
            db.session.commit()
        else:
            return render_template('errors.html', errors_text=str(form.errors))

        # redirect user to home page
        return redirect(url_for("login"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


if __name__ == '__main__':
    from models import *
    from forms import *

    db.create_all()

    reytyng.run()
