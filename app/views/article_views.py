from flask import Blueprint, make_response, jsonify, request, render_template, redirect, url_for
from app.models import Article
from app.forms.form import ArticleForm
from app.utilities.helpers import protected

blog = Article()

article = Blueprint('article', __name__)

@article.route('/article', methods=['POST', 'GET'])
@protected
def create_article(logged_user):
    form = ArticleForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        created_by= logged_user['email']
        article = {
            "title": title,
            "content": content,
            "created_by": created_by
        }
        blog.create_article(article)
        return '<h1>' + form.title.data + ' ' + form.content.data + '<h1>'
    return render_template('article.html', form=form)

@article.route('/', methods=['GET'])
def get_articles():
    """ fetch all articles """
    posts = blog.get_all_articles()
    if posts:
        return render_template('home.html', posts=posts)
        # return make_response(jsonify({'status': 200, 'article_list': articles}))
