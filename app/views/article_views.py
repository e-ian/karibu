from flask import Blueprint, make_response, jsonify, request, render_template, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from sqlalchemy import desc
from app.models import Article
from app.forms.form import ArticleForm
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
    return render_template('article.html', form=form)

@article.route('/', methods=['GET'])
def get_articles():
    """ fetch all articles """
    posts = Article.query.order_by(Article.created_on.desc())
    if posts:
        return render_template('home.html', posts=posts)

@article.route('/article/<int:article_id>')
def post(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('post.html', title=article.title, post=article)

@article.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_post(article_id):
    post = Article.query.get_or_404(article_id)
    if post.created_by != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('article.get_articles'))
