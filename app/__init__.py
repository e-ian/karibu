from flask import Flask
from .database import Database
from flask_bootstrap import Bootstrap
from config import app_config

def create_app(config_type = 'production'):
    ap = Flask(__name__)
    Bootstrap(ap)
    ap.config['SECRET_KEY'] = 'Alimanuakokoroapac'
    ap.config.from_object(app_config[config_type])
    Database()
    from app.views.user_views import user
    from app.views.article_views import article
    ap.register_blueprint(user)
    ap.register_blueprint(article)

    return ap
