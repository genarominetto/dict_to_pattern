from staff.staff_modules.service_modules.managers import Managers
from staff.staff_modules.service_modules.waiters import Waiters

class Service:
    def __init__(self):
        self.managers = Managers()
        self.waiters = Waiters()
