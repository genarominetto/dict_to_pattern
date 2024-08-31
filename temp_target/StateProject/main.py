from light_switch.light_switch import LightSwitch

if __name__ == "__main__":
    light_switch = LightSwitch() # (state: off)

    light_switch.set_state_to_on()
    light_switch.set_state_to_off()

    light_switch.additional_operation()
    light_switch.another_additional_operation()

    light_switch.report_status()
