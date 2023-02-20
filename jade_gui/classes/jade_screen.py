class JadeScreen:
    def __init__(self, set_valid):
        super().__init__()
        self._set_valid = set_valid

        self.valid = False

    def is_valid(self):
        return self.valid

    def set_valid(self, valid: bool):
        self.valid = valid
        self._set_valid(valid)

    def on_show(self):
        pass

    def on_complete(self):
        pass
