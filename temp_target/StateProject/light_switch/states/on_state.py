from light_switch.states.abstract.state import State

class OnState(State):
    def __init__(self):
        super().__init__()
        self.name = "On State"
        self.energy_saving_mode = None
        self.is_active = None

    def set_state_to_on(self, context):
        print(f"Already in {self.name}.")

    def set_state_to_off(self, context):
        print(f"Transition from {self.name} to Off state is not allowed.")

    def additional_operation(self):
        pass

    def another_additional_operation(self):
        pass
