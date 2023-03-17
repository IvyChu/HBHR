from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from flask_security import current_user, login_required
from hbhr import log, db
from hbhr.models import Service, Business, Address, Phone
from hbhr.main.forms import BusinessForm, AddressForm, PhoneForm
from hbhr.utils import save_thumbnail

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

@main.route("/business/new", methods=['GET', 'POST'])
@login_required
def new_business():
    form = BusinessForm()
    
    if form.validate_on_submit():
        business = Business(name=form.name.data, email=form.email.data, webpage=form.webpage.data, description=form.description.data)
        business.set_url(form.name.data)
        business.add_member(user=current_user, role=Business.OWNER)
        db.session.add(business)
        db.session.commit()

        log.info(f"Created business {business.id}")

        flash(f'Your business {business.name} has been created', 'success')
        return redirect(url_for('main.business', business_url=business.url))

    return render_template('business_new.html', title='New business',
                           form=form)

@main.route("/business/<int:business_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_business(business_id):
    log.info(f"{current_user.businesses}")
    business = Business.query.get_or_404(business_id)
    if not (current_user.is_owner(business_id) or current_user.has_role('admin')):
        flash("You don't have the permission to edit this business. Check with the business owner or admin.","warning")
        return redirect(url_for('main.business', business_url=business.id))

    form = BusinessForm()

    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_thumbnail(form.image_file.data)
            business.image_file = image_file
        business.name = form.name.data
        if form.url.data is None:
            business.set_url(form.name.data)
        else:
            business.set_url(form.url.data)
        business.email = form.email.data
        business.webpage = form.webpage.data
        business.description = form.description.data
        db.session.commit()
        flash('Your business has been updated!', 'success')
        return redirect(url_for('main.business', business_url=business.url))
    elif request.method == 'GET':
        form.name.data = business.name
        form.email.data = business.email
        form.url.data = business.url
        form.webpage.data = business.webpage
        form.description.data = business.description

    image_file = url_for('static', filename='profile_pics/' + business.image_file)

    return render_template('business_edit.html', title='Manage business',
                           form=form, business_id=business_id)


@main.route("/business/<string:business_url>", methods=['GET'])
def business(business_url):
    business = Business.query.filter_by(url=business_url).first()
    if not business:
        return render_template('errors/404.html')
    
    log.info(business.members)

    return render_template('business.html', title=business.name, business=business)


@main.route("/business/<int:business_id>/address/new", methods=['GET', 'POST'])
@login_required
def add_address(business_id):
    business = Business.query.get_or_404(business_id)
    # return the form for the address input
    form = AddressForm()
    if form.validate_on_submit():
        address = Address(address=form.address.data, city=form.city.data, state=form.state.data, zip=form.zip.data)
        business.addresses.append(address)
        db.session.commit()
        return render_template('address.html', address=address, business=business)
    
    return render_template("address_add.html", business_id=business_id, form=form)

@main.route("/address/<int:address_id>/edit", methods=['GET', 'PUT'])
@login_required
def edit_address(address_id):
    
    address = Address.query.get_or_404(address_id)
    business = Business.query.get_or_404(address.business_id)
    form = AddressForm()

    # PUT - update address, and return it in text form
    if form.validate_on_submit():
        address.address = form.address.data
        address.city = form.city.data
        address.state = form.state.data
        address.zip = form.zip.data
        db.session.commit()
        return render_template('address.html', address=address, business=business)
    
    # GET the address edit form
    form.address.data = address.address
    form.city.data = address.city
    form.state.data = address.state
    form.zip.data = address.zip
    return render_template("address_edit.html", address=address, form=form)

@main.route("/address/<int:address_id>", methods=['GET', 'PUT'])
def get_address(address_id):
    # if PUT - update the address
    # if GET - update was cancelled, so return what was there before
    address = Address.query.get_or_404(address_id)
    form = AddressForm()
    if form.validate_on_submit():
        address.address = form.address.data
        address.city = form.city.data
        address.state = form.state.data
        address.zip = form.zip.data
        db.session.commit()
        return render_template('address.html', address=address)
    return render_template('address.html', address=address)

@main.route("/address/<int:address_id>", methods=['DELETE'])
@login_required
def del_address(address_id):
    address = Address.query.get_or_404(address_id)
    if not current_user.is_owner(address.business_id):
        abort(403)
    db.session.delete(address)
    db.session.commit()
    return ''

@main.route("/business/<int:business_id>/phone/new", methods=['GET'])
@login_required
def add_phone(business_id):
    # return the form for the address input
    form = AddressForm()
    return render_template("address_add.html", business_id=business_id, form=form)