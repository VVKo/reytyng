# -*- coding: utf-8 -*-

from datetime import date

from reytyng import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    grupa_id = db.Column(db.Integer, db.ForeignKey('grupa.id'),
                          nullable=False)


    def __str__(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'stud': self.__str__(),
            'grupa': Grupa.query.filter_by(id=self.grupa_id).first().group_name
        }


class Grupa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='grupa', lazy=True)

    def __str__(self):
        return "{} група".format(self.group_name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'group': self.__str__(),
        }


class Kurator(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)

    def __str__(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'kurator': self.__str__(),
        }




class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    module_url = db.Column(db.String(350), unique=True, nullable=False)
    # tasks = db.relationship('Task', backref='module', lazy=True)

    def __init__(self, title, module_url):
        self.title = title
        self.module_url = module_url

    def __str__(self):
        return "Модуль: {}".format(self.title)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'tasks': "TODO",
            'tasks_count': self.tasks_count,
            # This is an example how to deal with Many2Many relations
            # 'many2many': self.serialize_many2many
        }

    @property
    def tasks_count(self):
        return Task.query.filter_by(module=self).count()

    @property
    def serialize_many2many(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        pass
        # return [item.serialize for item in self.tasks]


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer,
                          db.ForeignKey('module.id'),
                          nullable=False,
                          index=True)
    module = db.relationship(Module, foreign_keys=[module_id, ])
    task_url = db.Column(db.String(350), unique=True, nullable=False)
    content = db.Column(db.String(3000), nullable=False)
    answer_type = db.Column(db.String(15), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'content': self.content,
            'answer_type': self.answer_type,
        }


class AnswerChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ans1 = db.Column(db.String(200), nullable=True)
    is_True = db.Column(db.Boolean, nullable=True, default=False)
    task_id = db.Column(db.Integer,
                        db.ForeignKey('task.id'),
                        nullable=False,
                        index=True)
    task = db.relationship(Task, foreign_keys=[task_id, ])

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'question': self.ans1,
            'answer': self.is_True,
        }


class AnswerMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ans1 = db.Column(db.String(200), nullable=True)
    ans2 = db.Column(db.String(200), nullable=True)
    task_id = db.Column(db.Integer,
                        db.ForeignKey('task.id'),
                        nullable=False,
                        index=True)
    task = db.relationship(Task, foreign_keys=[task_id, ])

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'question': self.ans1,
            'answer': self.ans2,
        }


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    hash = db.Column(db.String)