# coding=utf-8


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(U'邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    password = PasswordField(U'密码', validators=[Required()])
    remember_me = BooleanField(U'记住我')
    submit = SubmitField(U'登陆')


class RegistrationForm(FlaskForm):
    email = StringField(U'邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    username = StringField(U'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField(U'密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(U'确认密码', validators=[Required()])
    submit = SubmitField(U'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(U'邮箱已注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(U'用户名已被使用')



class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(U'旧密码', validators=[Required()])
    password = PasswordField(U'新密码', validators=[
        Required(), EqualTo(U'密码2', message=U'密码必须匹配')])
    password2 = PasswordField(U'确认密码', validators=[Required()])
    submit = SubmitField(U'更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField(U'邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    submit = SubmitField(U'重设密码')


class PasswordResetForm(FlaskForm):
    email = StringField(U'邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    password = PasswordField(U'新密码', validators=[
        Required(), EqualTo(U'密码2', message='Passwords must match')])
    password2 = PasswordField(U'确认密码', validators=[Required()])
    submit = SubmitField(U'重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(U'未知邮箱地址')


class ChangeEmailForm(FlaskForm):
    email = StringField(U'新邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField(U'密码', validators=[Required()])
    submit = SubmitField(U'更新邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(U'邮箱已注册')
