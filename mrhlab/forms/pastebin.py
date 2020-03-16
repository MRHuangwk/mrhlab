from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

from mrhlab.extensions import db

class GenerateForm(FlaskForm):
    original = StringField('Original Content: ', validators=[DataRequired()])
    submit = SubmitField('Submit')