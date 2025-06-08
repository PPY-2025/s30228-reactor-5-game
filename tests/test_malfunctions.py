import pytest
from game_engine.reactor import ReactorCore

def test_coolant_leak():
    reactor = ReactorCore(enable_random_events=False)
    reactor.add_malfunction("Coolant Leak", 3,
                            reactor.coolant_leak_effect,
                            reactor.fix_coolant_leak)
    start_coolant = reactor.coolant
    for _ in range(3):
        reactor.tick()
    assert reactor.coolant == start_coolant - 15
    assert not reactor.active_malfunctions

def test_valve_jam():
    reactor = ReactorCore(enable_random_events=False)
    reactor.pressure = 50
    reactor.add_malfunction("Valve Jam", 2,
                            reactor.valve_jam_effect,
                            reactor.unjam_valve)
    reactor.tick()
    reactor.release_pressure()
    assert reactor.pressure == 57
    reactor.tick()
    reactor.tick()
    reactor.release_pressure()
    assert reactor.pressure < 72

def test_power_surge():
    reactor = ReactorCore(enable_random_events=False)
    base = reactor.heat
    reactor.add_malfunction("Power Surge", 2,
                            reactor.power_surge_effect,
                            reactor.reset_circuit)
    reactor.tick()
    assert reactor.heat >= base + 15
    reactor.tick()
    assert reactor.active_malfunctions == []

def test_sensor_malfunction():
    reactor = ReactorCore(enable_random_events=False)
    reactor.add_malfunction("Sensor Malfunction", 2,
                            reactor.sensor_malfunction_effect,
                            reactor.calibrate_sensors)
    reactor.tick()
    assert reactor.sensor_fault
    reactor.tick()
    reactor.tick()
    assert not reactor.sensor_fault

def test_control_lockout():
    reactor = ReactorCore(enable_random_events=False)
    reactor.add_malfunction("Control Lockout", 2,
                            reactor.control_lockout_effect,
                            reactor.override_lockdown)
    reactor.tick()
    assert reactor.controls_locked
    reactor.tick()
    reactor.tick()
    assert not reactor.controls_locked