class EntityData:
    def __init__(self, hud, name, entity_type, state, position):
        self.hud = hud
        self.name = name
        self.type = entity_type

        self._state = state
        self.position = position

        self._score = 0
        self.winner = None

        self.hud.add_data(self)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        if self.state == "death":
            self.hud.delete_elements(self)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        if self.score == 3:
            self.winner = self