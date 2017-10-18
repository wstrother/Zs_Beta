from src.graphics import TextGraphics
from src.entities import Sprite


class TextSprite(Sprite):
    def __init__(self, name):
        super(TextSprite, self).__init__(name)
        self.graphics = TextGraphics(self, "")

        self.text = ""

    def set_text(self, text):
        self.text = text
        self.graphics.set_text(text)
