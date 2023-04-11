from hbhr import db
from hbhr.users.forms import UpdateAccountForm
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import current_user, login_required, AnonymousUser
from hbhr.utils import save_thumbnail
from hbhr.models import User

users = Blueprint('users', __name__)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_thumbnail(form.picture.data)
            current_user.image_file = picture_file
        current_user.set_username(form.username.data)
        current_user.email = form.email.data
        current_user.display_name = form.display_name.data
        current_user.notes = form.notes.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.display_name.data = current_user.display_name
        form.notes.data = current_user.notes
        form.location.data = current_user.location
    return render_template('account.html', title='Account',
                           form=form, user=current_user)


@users.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Account',
                           user=current_user)


@users.route("/user/<string:username>", methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template('errors/404.html')

    return render_template('profile_page.html', user=user)
