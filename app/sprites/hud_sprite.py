from src.graphics import TextGraphics
from app.sprites.text_sprite import TextSprite


class HudSprite(TextSprite):
    def __init__(self, name):
        super(HudSprite, self).__init__(name)
        self.graphics = TextGraphics(self, "")

        self.hud_field = None

    def set_hud_field(self, target, attribute):
        self.hud_field = target, attribute
