from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from app.models import db

def create_app(config_type = 'production'):
    ap = Flask(__name__)
    Bootstrap(ap)
    ap.config['SECRET_KEY'] = 'Alimanuakokoroapac'
    ap.config.from_object(app_config[config_type])
    db.init_app(ap)
    from app.models import Users, Article
    from app.views.user_views import user
    from app.views.article_views import article
    ap.register_blueprint(user)
    ap.register_blueprint(article)

    return ap

