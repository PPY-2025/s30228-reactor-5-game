import random
from game_engine.malfunction import *

class ReactorCore:
    def __init__(self, enable_random_events=True):
        self.heat = 0
        self.pressure = 0
        self.coolant = 100
        self.time_alive = 0
        self.cool_down_cooldown = 0  # ticks until next cooldown allowed
        self.pressure_release_cooldown = 0
        self.active_malfunctions = []
        self.malfunction = False
        self.valve_jammed = False
        self.sensor_fault = False
        self.controls_locked = False
        self.enable_random_events = enable_random_events
        self.red_button = False

    # cool down the reactor
    def cool_down(self):
        if self.coolant > 0 and self.cool_down_cooldown == 0:
            self.heat = max(0, self.heat - 10)
            self.coolant -= 10
            self.cool_down_cooldown = 2

    # release pressure from the reactor
    def release_pressure(self):
        if not self.valve_jammed and self.pressure_release_cooldown == 0:
            self.pressure = max(0, self.pressure - 15)
            self.pressure_release_cooldown = 2

    def tick(self, passive=True):
        self.time_alive += 1
        if passive:
            self.heat += 5
            self.pressure += 7

        if self.cool_down_cooldown > 0:
            self.cool_down_cooldown -= 1
        if self.pressure_release_cooldown > 0:
            self.pressure_release_cooldown -= 1

        for malfunction in self.active_malfunctions[:]:
            malfunction.apply_effect(self)
            if malfunction.is_expired():
                self.malfunction = False
                malfunction.fix_fn()

        # 20% chance to trigger a random malfunction if none active
        if self.enable_random_events and not self.active_malfunctions and random.random() < 0.2:
            self.trigger_random_malfunction()

    def trigger_random_malfunction(self):
        options = [
            ("Coolant Leak", 3, self.coolant_leak_effect, self.fix_coolant_leak),
            ("Valve Jam", 4, self.valve_jam_effect, self.unjam_valve),
            ("Power Surge", 2, self.power_surge_effect, self.reset_circuit),
            ("Sensor Malfunction", 3, self.sensor_malfunction_effect, self.calibrate_sensors),
            ("Control Lockout", 3, self.control_lockout_effect, self.override_lockdown),
        ]
        name, duration, eff, fix = random.choice(options)
        self.add_malfunction(name, duration, eff, fix)
        self.malfunction = True

    def add_malfunction(self, name, duration, effect_fn, fix_fn):
        mal = Malfunction(name, duration, effect_fn, fix_fn)
        self.active_malfunctions.append(mal)

    # Malfunctions

    def coolant_leak_effect(self, reactor):
        reactor.coolant = max(0, reactor.coolant - 5)

    def valve_jam_effect(self, reactor):
        reactor.valve_jammed = True

    def power_surge_effect(self, reactor):
        reactor.heat += 10

    def sensor_malfunction_effect(self, reactor):
        reactor.sensor_fault = True

    def control_lockout_effect(self, reactor):
        reactor.controls_locked = True

    # Fixes

    def fix_coolant_leak(self):
        if not any(m.name == "Coolant Leak" for m in self.active_malfunctions):
            return
        self.active_malfunctions = [m for m in self.active_malfunctions if m.name != "Coolant Leak"]
        self.malfunction = False

    def unjam_valve(self):
        if not any(m.name == "Valve Jam" for m in self.active_malfunctions):
            return
        self.active_malfunctions = [m for m in self.active_malfunctions if m.name != "Valve Jam"]
        self.malfunction = False
        self.valve_jammed = False
        self.pressure = max(0, self.pressure - 5)

    def reset_circuit(self):
        if not any(m.name == "Power Surge" for m in self.active_malfunctions):
            return
        self.active_malfunctions = [m for m in self.active_malfunctions if m.name != "Power Surge"]
        self.malfunction = False
        self.heat = max(0, self.heat - 10)

    def calibrate_sensors(self):
        if not any(m.name == "Sensor Malfunction" for m in self.active_malfunctions):
            return
        self.active_malfunctions = [m for m in self.active_malfunctions if m.name != "Sensor Malfunction"]
        self.malfunction = False
        self.sensor_fault = False

    def override_lockdown(self):
        if not any(m.name == "Control Lockout" for m in self.active_malfunctions):
            return
        self.active_malfunctions = [m for m in self.active_malfunctions if m.name != "Control Lockout"]
        self.malfunction = False
        self.controls_locked = False