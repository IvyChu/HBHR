from flask import render_template, request, Blueprint
from flask_security import current_user

admin = Blueprint('admin', __name__)


@admin.route("/admin")
def home():
    return render_template('index.html', title='Admin')