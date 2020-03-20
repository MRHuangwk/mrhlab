from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import  SubmitField, RadioField
from wtforms.validators import DataRequired

from mrhlab.extensions import db

class TransferForm(FlaskForm):
    style = RadioField('style', choices=[('starrynight', 'Starry Night'), ('thescream', 'The Scream')], validators=[DataRequired()])
    photo = FileField('Upload Image', validators=[DataRequired(), FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField('Submit')