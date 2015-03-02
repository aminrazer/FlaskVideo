from flask.ext.wtf import Form
from wtforms import StringField, TextField, SubmitField, validators, TextAreaField
from wtforms.validators import Required, DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.wtf.recaptcha import RecaptchaField

class videoUploadForm(Form):
	Title =  TextField('Title', [validators.Required("Please enter a Title"), validators.Length(min=0, max=100)])
	Description = TextAreaField('Description', [validators.Length(min=0, max=100)])

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class SubtitleForm(Form):
	sub = TextAreaField('',[validators.Length(min=0, max=100)])