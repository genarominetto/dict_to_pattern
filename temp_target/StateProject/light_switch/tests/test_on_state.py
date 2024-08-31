import pytest
from light_switch.states.off_state import OffState
from light_switch.states.on_state import OnState
from light_switch.light_switch import LightSwitch

def test_transition_from_on_to_on():
    light_switch = LightSwitch()
    light_switch._state = OnState()
    assert isinstance(light_switch._state, OnState)
    light_switch.set_state_to_on()
    assert isinstance(light_switch._state, OnState)

def test_transition_from_on_to_off():
    light_switch = LightSwitch()
    light_switch._state = OnState()
    assert isinstance(light_switch._state, OnState)
    light_switch.set_state_to_off()
    assert isinstance(light_switch._state, OnState)
