import pytest
from game_engine.reactor import ReactorCore

def test_fix_coolant_leak():
    reactor = ReactorCore()
    reactor.add_malfunction("Coolant Leak", 3,
                            reactor.coolant_leak_effect,
                            reactor.fix_coolant_leak)
    reactor.tick()
    coolant_before_fix = reactor.coolant
    reactor.fix_coolant_leak()

    assert all(m.name != "Coolant Leak" for m in reactor.active_malfunctions)

    reactor.tick()
    assert reactor.coolant == coolant_before_fix

def test_fix_valve_jam():
    reactor = ReactorCore()
    reactor.add_malfunction("Valve Jam", 2,
                            reactor.valve_jam_effect,
                            reactor.unjam_valve)
    reactor.tick()
    reactor.unjam_valve()

    assert all(m.name != "Valve Jam" for m in reactor.active_malfunctions)

def test_fix_power_surge():
    reactor = ReactorCore()
    reactor.add_malfunction("Power Surge", 2,
                            reactor.power_surge_effect,
                            reactor.reset_circuit)
    reactor.tick()
    reactor.reset_circuit()

    assert all(m.name != "Power Surge" for m in reactor.active_malfunctions)

def test_fix_sensor_fault():
    reactor = ReactorCore()
    reactor.add_malfunction("Sensor Malfunction", 2,
                            reactor.sensor_malfunction_effect,
                            reactor.calibrate_sensors)
    reactor.tick()
    reactor.calibrate_sensors()

    assert all(m.name != "Sensor Malfunction" for m in reactor.active_malfunctions)

def test_fix_lockdown_protocol():
    reactor = ReactorCore()
    reactor.add_malfunction("Control Lockout", 2,
                            reactor.control_lockout_effect,
                            reactor.override_lockdown)
    reactor.tick()
    reactor.override_lockdown()

    assert all(m.name != "Control Lockout" for m in reactor.active_malfunctions)