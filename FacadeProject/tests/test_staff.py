import pytest
from staff.staff import Staff

@pytest.fixture
def staff():
    return Staff()

def test_staff_kitchen_chefs_operation(staff):
    staff.staff.kitchen.chefs.operation()
    # Add assertions or checks if needed

def test_staff_kitchen_helpers_operation(staff):
    staff.staff.kitchen.helpers.operation()
    # Add assertions or checks if needed

def test_staff_service_managers_operation(staff):
    staff.staff.service.managers.operation()
    # Add assertions or checks if needed

def test_staff_service_waiters_operation(staff):
    staff.staff.service.waiters.operation()
    # Add assertions or checks if needed
