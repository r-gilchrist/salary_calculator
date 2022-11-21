from flask import Flask

from salary_calculator.endpoints import salary_breakdown_request


def create_app() -> Flask:

    app = Flask(__name__)
    setup_endpoints(app)

    return app


def setup_endpoints(app: Flask):
    app.register_blueprint(salary_breakdown_request.bp)
