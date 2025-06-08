class Malfunction:
    def __init__(self, name, duration, effect_fn, fix_fn):
        self.name = name
        self.duration = duration
        self.effect_fn = effect_fn # modifies the reactor state
        self.fix_fn = fix_fn       # fixes malfunction

    def apply_effect(self, reactor):
        self.effect_fn(reactor)
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0