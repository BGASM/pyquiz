import os
from loguru import logger
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    test = os.path.join(app.instance_path, 'msucom_qbank.sqlite')
    logger.debug(test)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=test,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from msucom_qbank import db
    db.init_app(app)

    from msucom_qbank import auth, quiz
    app.register_blueprint(auth.bp)
    app.register_blueprint(quiz.bp)

    app.add_url_rule("/", endpoint="index")

    return app
