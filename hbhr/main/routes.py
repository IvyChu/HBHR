from flask import render_template, request, Blueprint
from flask_security import current_user
from hbhr import log
from hbhr.models import Service

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    log.debug("We've hit home")
    services = Service.query.all()
    return render_template('index.html', title='Welcome', services=services)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/privacy")
def privacy():
    return render_template('privacy.html', title='Privacy policy')