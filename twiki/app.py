"""
    twiki
    ~~~~~
    Unified search client for twitter and wikipedia
"""

from flask import Blueprint, redirect, render_template, url_for, jsonify
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from .exts import twitter, wiki


frontend = Blueprint('frontend', __name__)
backend = Blueprint('backend', __name__)


class SearchForm(Form):
    term = StringField(label='What do you want to search for?',
                       validators=[DataRequired()])
    submit = SubmitField(label="Let's go find it!")


@frontend.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        term = form.term.data
        anchor = '#/#{0}'.format(term)
        return redirect(url_for('.search') + anchor)
    return render_template('index.html', form=form)


@frontend.route('/search/')
def search():
    return render_template('display_results.html')


@backend.route('/tweets/<term>')
def tweets(term=None):
    if term is None:
        return jsonify({'msg': 'no search term provided'}), 400

    return jsonify(tweets=twitter.search(term))


@backend.route('/titles/<term>')
def titles(term=None):
    if term is None:
        return jsonify({'msg': 'no search term provided'}), 400

    return jsonify(titles=wiki.search(term))


@backend.route('/page/<title>')
def page(title=None):
    if title is None:
        return jsonify({'msg': 'no page title provided'}), 400
    return jsonify(page=wiki.get_page(title))
