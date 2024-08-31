from light_switch.states.off_state import OffState
from light_switch.states.on_state import OnState

class LightSwitch:
    def __init__(self):
        self._state = OffState()

    def set_state_to_on(self):
        self._state.set_state_to_on(self)

    def set_state_to_off(self):
        self._state.set_state_to_off(self)

    def additional_operation(self):
        self._state.additional_operation()

    def another_additional_operation(self):
        self._state.another_additional_operation()

    def report_status(self):
        print(self._state)
