from flask import url_for, redirect, render_template

from .models import URLModel
from .forms import URLForm
from . import app, db


import random
import string


def get_short(original_url):
    while True:
        short = ''.join(random.sample(string.ascii_letters+string.ascii_lowercase+string.ascii_uppercase, 6))
        if URLModel.query.filter(URLModel.short == short).first():
            continue
        return short


@app.route('/', methods=['POST', 'GET'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = URLModel()
        url.original_url = form.original_url.data
        url.short = get_short(url.original_url)
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('urls'))
    return render_template('index.html', form=form)


@app.route('/urls')
def urls():
    urls = URLModel.query.all()
    return render_template('urls.html', urls=urls)


@app.route('/<short>')
def url_redirect(short):
    url = URLModel.query.filter(URLModel.short == short).first()
    if url:
        url.visits += 1
        db.session.add(url)
        db.session.commit()
        return redirect(url.original_url) 