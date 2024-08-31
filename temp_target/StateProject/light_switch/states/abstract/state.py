class State:
    def __init__(self):
        self.name = None
        self.energy_saving_mode = None
        self.is_active = None

    def set_state_to_on(self, context):
        raise NotImplementedError

    def set_state_to_off(self, context):
        raise NotImplementedError

    def additional_operation(self):
        raise NotImplementedError

    def another_additional_operation(self):
        raise NotImplementedError

    def __str__(self):
        return f"State: {self.name}\n- Energy saving: {self.energy_saving_mode}\n- Active: {self.is_active}"
