from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DeckForm(FlaskForm):
    deck1 = StringField('Deck1', validators=[DataRequired()])
    deck2 = StringField('Deck2', validators=[DataRequired()])
    submit = SubmitField('Submit')
