import pytest
from game_engine.reactor import ReactorCore

def test_initial_state():
    reactor = ReactorCore()
    assert reactor.heat == 0
    assert reactor.pressure == 0
    assert reactor.coolant == 100
    assert reactor.time_alive == 0

def test_cool_down():
    reactor = ReactorCore()
    reactor.heat = 50
    reactor.cool_down()
    assert reactor.heat == 40
    assert reactor.coolant == 90

def test_release_pressure():
    reactor = ReactorCore()
    reactor.pressure = 30
    reactor.release_pressure()
    assert reactor.pressure == 15

def test_tick_increases_stats():
    reactor = ReactorCore()
    reactor.tick()
    assert reactor.heat == 5
    assert reactor.pressure == 7
    assert reactor.time_alive == 1

def test_cool_down_cooldown():
    reactor = ReactorCore(enable_random_events=False)
    reactor.coolant = 50
    reactor.heat = 50

    reactor.cool_down()
    assert reactor.heat == 40
    assert reactor.coolant == 40
    assert reactor.cool_down_cooldown > 0

    reactor.cool_down()
    assert reactor.heat == 40
    assert reactor.coolant == 40

    for _ in range(reactor.cool_down_cooldown):
        reactor.tick(passive=False)

    reactor.cool_down()
    assert reactor.heat == 30
    assert reactor.coolant == 30

def test_release_pressure_cooldown():
    reactor = ReactorCore(enable_random_events=False)
    reactor.pressure = 50
    reactor.valve_jammed = False

    reactor.release_pressure()
    assert reactor.pressure == 35
    assert reactor.pressure_release_cooldown > 0
    reactor.release_pressure()
    assert reactor.pressure == 35

    for _ in range(reactor.pressure_release_cooldown):
        reactor.tick(passive=False)

    reactor.release_pressure()
    assert reactor.pressure == 20