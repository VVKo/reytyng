# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import fields, validators
from wtforms_alchemy import ModelForm

from models import Module, Task, AnswerChoice, Users, AnswerMatch, Student, Kurator, Grupa


class UsersForm(ModelForm):
    class Meta:
        model = Users


class ModuleForm(ModelForm):
    class Meta:
        model = Module


class StudentForm(ModelForm):
    class Meta:
        model = Student


class KuratorForm(ModelForm):
    class Meta:
        model = Kurator


class GrupaForm(ModelForm):
    class Meta:
        model = Grupa


class TaskForm(ModelForm):
    class Meta:
        model = Task
        include = [
            'module_id',
        ]


class AnswerChoiceForm(ModelForm):
    class Meta:
        model = AnswerChoice
        include = [
            'task_id',
        ]


class AnswerMatchForm(ModelForm):
    class Meta:
        model = AnswerMatch
        include = [
            'task_id',
        ]


