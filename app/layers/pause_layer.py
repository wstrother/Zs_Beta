from src.entities import Layer


class PauseLayer(Layer):
    def __init__(self, name):
        super(PauseLayer, self).__init__(name)

        self.paused = True
        self.visible = False

    def on_pause(self):
        super(PauseLayer, self).on_pause()
        self.visible = not self.paused
