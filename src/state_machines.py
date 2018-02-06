class StateMachine:
    def __init__(self, state_data):
        self.data = state_data
        self.state = list(state_data.keys())[0]

    def set_state(self, state):
        self.state = state

    @property
    def state_data(self):
        if self.state in self.data:
            return self.data[self.state]

    def update(self):
        if self.state_data:
            conditions = self.state_data["conditions"]

            for c in conditions:
                if c["test"]():
                    self.set_state(c["to"])
