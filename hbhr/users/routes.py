from hbhr import db
from hbhr.users.forms import UpdateAccountForm
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import current_user, login_required
from hbhr.utils import save_thumbnail

users = Blueprint('users', __name__)

@login_required
@users.route("/account", methods=['GET', 'POST'])
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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, user=current_user)


