from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, DeckForm
import GetCSV

@app.route('/')
@app.route('/index')
def index():
    user = {"username": "Nick"}
    posts = [
        {
            'author' : {'username' : 'john' },
            'body' : 'Beautiful day in the neighborhood!'
        },
        {
            'author' : {'username' : 'susan' },
            'body' : 'I hate the neighborhood.'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/other')
def other():
    user = {"username": "Nick"}
    posts = [
        {
            'author' : {'username' : 'john' },
            'body' : 'Beautiful day in the neighborhood!'
        },
        {
            'author' : {'username' : 'susan' },
            'body' : 'I hate the fucking neighborhood.'
        }
    ]
    return render_template('other.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requrested for user {}, remember me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/input', methods=['GET', 'POST'])
def input():
    form = DeckForm()
    if form.validate_on_submit():
        flash('Deck1: {}, Deck2: {}'.format(form.deck1.data, form.deck2.data))
        deck = GetCSV.calc_deck_diff([form.deck1.data, form.deck2.data])
        # return redirect('/index')
        return render_template('input.html', title="go buy these", form=form, deck=deck)
    return render_template('input.html', title='Input Decks', form=form)