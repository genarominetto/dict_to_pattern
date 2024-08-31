from light_switch.states.abstract.state import State

class OffState(State):
    def __init__(self):
        super().__init__()
        self.name = "Off State"
        self.energy_saving_mode = None
        self.is_active = None

    def set_state_to_on(self, context):
        print(f"Switching from {self.name} to On state.")
        context._state = OnState()

    def set_state_to_off(self, context):
        print(f"Already in {self.name}.")

    def additional_operation(self):
        pass

    def another_additional_operation(self):
        pass

# Import OnState to resolve the forward reference
from light_switch.states.on_state import OnState
