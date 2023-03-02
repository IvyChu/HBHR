from flask import render_template, request, Blueprint, flash
from flask_security import current_user, roles_accepted
from hbhr.models import User, Service
from hbhr import db, user_datastore
from hbhr.admin.forms import ServiceForm

admin = Blueprint('admin', __name__)


@admin.route("/admin")
@roles_accepted('admin')
def home():
    return render_template('admin/admin.html', title='Admin')

@admin.route("/admin/services/<int:service_id>/edit", methods=['GET'])
@roles_accepted('admin')
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()    
    form.name.data = service.name
    form.description.data = service.description
    return render_template('admin/service_edit.html', service=service, form=form)

@admin.route("/admin/services/", methods=['POST'])
@roles_accepted('admin')
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(name=form.name.data, description=form.description.data)
        db.session.add(service)
        db.session.commit()
        return render_template('admin/service_row.html', service=service)
    return "Error encountered while adding a service."

@admin.route("/admin/services/<int:service_id>", methods=['DELETE'])
@roles_accepted('admin')
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return ''

@admin.route("/admin/services/<int:service_id>", methods=['GET', 'PUT'])
@roles_accepted('admin')
def get_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        db.session.commit()
        return render_template('admin/service_row.html', service=service)
    return render_template('admin/service_row.html', service=service)


@admin.route("/admin/services")
@roles_accepted('admin')
def services():

    services = Service.query.all()
    form = ServiceForm()

    return render_template('admin/services.html', title='Edit services', services=services, form=form)
