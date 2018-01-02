# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField(u'发表你的想法？', validators=[Required()])
    submit = SubmitField(U'提交')


class EditProfileForm(FlaskForm):
    name = StringField(U'真实姓名', validators=[Length(0, 64)])
    location = StringField(U'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(U'简介')
    submit = SubmitField(U'提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField(U'邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    username = StringField(U'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField(U'验证')
    role = SelectField('Role', coerce=int)
    name = StringField(U'真实姓名', validators=[Length(0, 64)])
    location = StringField(U'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(U'简介')
    submit = SubmitField(U'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(U'邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(U'用户名已被使用')


class PostForm(FlaskForm):
    body = PageDownField(U"发表你的想法？", validators=[Required()])
    submit = SubmitField(U'提交')


class CommentForm(FlaskForm):
    body = StringField(U'提交评论', validators=[Required()])
    submit = SubmitField(U'提交')
