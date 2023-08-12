from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    rating = StringField('Your Rating 0ut of 10 e.g 7.5:', validators=[DataRequired()])
    review = StringField('Your Review:', validators=[DataRequired()])
    submit = SubmitField()


class AddMovie(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')
