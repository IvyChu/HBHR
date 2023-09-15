"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from hbhr.models import Business, Service, Address, Phone


def test_new_business():
    """
    GIVEN a Business model
    WHEN a new Business is created
    THEN check the name, description, email, webpage, status fields are defined correctly
    """
    business = Business(name="New biz", email="me@pm.me",
                        webpage="https://carefor.me", description="This is great.", status=Business.INACTIVE)
    assert business.name == 'New biz'
    assert business.email == 'me@pm.me'
    assert business.webpage == "https://carefor.me"
    assert business.description == "This is great."
    assert business.status == business.INACTIVE


def test_new_service():
    """
    GIVEN a Service model
    WHEN a new Service is created
    THEN check the name, description, email, webpage, image_file, status fields are defined correctly
    """
    service = Service(name="Midwifery", description="Helping mothers give brith")
    assert service.name == "Midwifery"
    assert service.description == "Helping mothers give brith"

def test_new_address():
    """
    GIVEN a Address model
    WHEN a new Address is created
    THEN check the address, city, state, zip fields are defined correctly
    """
    addr = Address(address="123 My Way", city="Merlin", state="New York", zip="12345")
    assert addr.address == "123 My Way"
    assert addr.city == "Merlin"
    assert addr.state == "New York"
    assert addr.zip == "12345"

def test_new_phone():
    """
    GIVEN a Phone model
    WHEN a new Phone is created
    THEN check the country_code, phone_number, extension fields are defined correctly
    """
    phone = Phone(country_code="+1", phone_number="1234567890",extension="3241")
    assert phone.country_code == "+1"
    assert phone.phone_number == "1234567890"
    assert phone.extension == "3241"
    