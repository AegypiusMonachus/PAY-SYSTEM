# from manager import app
from run import app


def job_func():
    with app.app_context():
        pass