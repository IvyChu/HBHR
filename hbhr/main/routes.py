from flask import render_template, request, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html', title='Welcome')