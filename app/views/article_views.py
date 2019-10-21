from flask import Blueprint, make_response, jsonify, request, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import Article
from app.forms.form import ArticleForm
from app.utilities.helpers import protected
from app import db

blog = Article()

article = Blueprint('article', __name__)

@article.route('/article', methods=['POST', 'GET'])
@login_required
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        created_by=current_user.username
        article = Article(
            title=title,
            content=content,
            created_by=created_by
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article.get_articles'))
        # return '<h1>' + form.title.data + ' ' + form.content.data + '<h1>'
    return render_template('article.html', form=form)

@article.route('/', methods=['GET'])
def get_articles():
    """ fetch all articles """
    posts = Article.query.all()
    if posts:
        return render_template('home.html', posts=posts)
