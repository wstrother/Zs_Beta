from src.entities import Layer


class PauseLayer(Layer):
    def __init__(self, name):
        super(PauseLayer, self).__init__(name)

        self.paused = True
        self.visible = False

    def handle_pause(self):
        self.paused = not self.paused
        self.visible = not self.paused
