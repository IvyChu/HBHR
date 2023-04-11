from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from flask_security import current_user, login_required, AnonymousUser
from hbhr import log, db
from hbhr.models import Service, Business, Address, Phone
from hbhr.main.forms import BusinessForm, AddressForm, PhoneForm, LinkServicesForm
from hbhr.utils import save_thumbnail
import phonenumbers 
from sqlalchemy import or_

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    log.debug("We've hit home")
    services = Service.query.filter_by(status=Service.ACTIVE)
    return render_template('index.html', title='Welcome', services=services)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/privacy")
def privacy():
    return render_template('privacy.html', title='Privacy policy')


@main.route('/search')
def search():
    search_terms = request.args.get('q').lower()

    # Search the Services table for service names and descriptions
    services = Service.query.filter(or_(
        Service.name.ilike(f'%{search_terms}%'),
        Service.description.ilike(f'%{search_terms}%'))
    ).all()

    businesses = []

    # Get the businesses that provide the services that match the search terms
    for service in services:
        if service.is_active():
            for business in service.businesses:
                if business.is_active():
                    businesses.append(business)

    log.debug(businesses)

    # Search the Business table for business names that match the search terms
    businesses += Business.query.filter(Business.name.ilike(f'%{search_terms}%')).all()

    # Remove duplicates
    businesses = list(set(businesses))

    return render_template('search_results.html', businesses=businesses, search_terms=search_terms)


@main.route('/service/<int:service_id>')
def service(service_id):
    # Get service with provided ID from the database or return a 404 error if it doesn't exist.
    service = Service.query.get_or_404(service_id)

    # If the service is not active, return a page with no businesses and the service information.
    if not service.is_active():
        return render_template('search_results.html', businesses=None, service=service)

    # Create an empty list to hold the businesses associated with the service.
    businesses = []

    # Loop through all the businesses associated with the service and append the active ones to the list.
    for business in service.businesses:
        if business.is_active():
            businesses.append(business)

    # Return a page displaying the businesses associated with the service and the service information.
    return render_template('search_results.html', businesses=businesses, service=service)


################
### BUSINESS ###
################


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
    
    if business.status == business.INACTIVE:
        if isinstance(current_user, AnonymousUser) or not (current_user.is_owner(business.id) or current_user.has_role('admin')):
            return render_template('errors/404.html')

    return render_template('business.html', title=business.name, business=business)

@main.route("/business/<int:business_id>/status", methods=['PUT'])
def toggle_business_status(business_id):
    # Get the business with the given ID or return a 404 error if not found
    business = Business.query.get_or_404(business_id)
    
    # Toggle the status of the service (i.e. change from active to inactive or vice versa)
    business.toggle_status()
    
    # Commit the changes to the database
    db.session.commit()
    
    # Render the template for the updated service row
    return render_template('business_status_button.html', business=business)


#################
### ADDRESSES ###
#################

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
    if not (current_user.is_owner(address.business_id) or current_user.has_role('admin')):
        abort(403)
    db.session.delete(address)
    db.session.commit()
    return ''


##############
### PHONES ###
##############

@main.route("/business/<int:business_id>/phone/new", methods=['GET', 'POST'])
@login_required
def add_phone(business_id):
    business = Business.query.get_or_404(business_id)
    # return the form for the phone input
    form = PhoneForm()
    if form.validate_on_submit():
        phone_number_parsed = phonenumbers.parse(form.phone_number.data, "US")
        phone = Phone(phone_number=phone_number_parsed.national_number, extension=phone_number_parsed.extension)
        business.phones.append(phone)
        db.session.commit()
        return render_template('phone.html', phone=phone, business=business)
    
    return render_template("phone_add.html", business_id=business_id, form=form)

@main.route("/phone/<int:phone_id>/edit", methods=['GET', 'PUT'])
@login_required
def edit_phone(phone_id):
    
    phone = Phone.query.get_or_404(phone_id)
    business = Business.query.get_or_404(phone.business_id)
    form = PhoneForm()

    # PUT - update phone, and return it in text form
    if form.validate_on_submit():
        phone_number_parsed = phonenumbers.parse(form.phone_number.data, "US")
        phone.phone_number = phone_number_parsed.national_number
        phone.extension = phone_number_parsed.extension
        db.session.commit()
        return render_template('phone.html', phone=phone, business=business)
    
    # GET the phone edit form
    parsed_number = phone.get_parsed()
    form.phone_number.data = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)

    return render_template("phone_edit.html", phone=phone, form=form)

@main.route("/phone/<int:phone_id>", methods=['GET', 'PUT'])
def get_phone(phone_id):
    # if PUT - update the phone
    # if GET - update was cancelled, so return what was there before
    phone = Phone.query.get_or_404(phone_id)
    form = PhoneForm()
    if form.validate_on_submit():
        phone_number_parsed = phonenumbers.parse(form.phone_number.data, "US")
        phone.phone_number = phone_number_parsed.national_number
        phone.extension = phone_number_parsed.extension
        db.session.commit()
        return render_template('phone.html', phone=phone)
    parsed_number = phone.get_parsed()
    return render_template('phone.html', phone=phone, phone_formatted=phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL))

@main.route("/phone/<int:phone_id>", methods=['DELETE'])
@login_required
def del_phone(phone_id):
    phone = Phone.query.get_or_404(phone_id)
    if not (current_user.is_owner(phone.business_id) or current_user.has_role('admin')):
        abort(403)
    db.session.delete(phone)
    db.session.commit()
    return ''


################
### SERVICES ###
################

@main.route("/business/<int:business_id>/services", methods=['GET', 'POST'])
@login_required
def edit_services(business_id):
    if not (current_user.is_owner(business_id) or current_user.has_role('admin')):
        abort(403)

    business = Business.query.get_or_404(business_id)

    services = Service.query.filter_by(status=Service.ACTIVE)

    form = LinkServicesForm()

    form.services.choices = [(s.id, f"{s.name}") for s in services ]

    if form.validate_on_submit():
        # Remove all previously selected services
        business.services = []

        # Services tagged
        form_services = form.services.data

        # Add the ones that have been selected this time
        for service in services:
            if service.id in form_services:
                business.services.append(service)

        # Commit changes to the database        
        db.session.commit()

        return render_template('services_list.html', business=business)

    elif request.method == 'GET':
        form.services.data = [(c.id) for c in business.services]

    return render_template("services_edit.html", form=form, business_id=business_id)
