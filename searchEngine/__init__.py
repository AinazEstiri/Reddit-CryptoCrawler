from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'project172'

    from .phase2 import views
    from .phase2 import display

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(display, url_prefix='/')

    return app

