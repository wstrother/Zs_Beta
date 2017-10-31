from app.sprites.gui_sprites import TextSprite


class HudSprite(TextSprite):
    def __init__(self, name):
        super(HudSprite, self).__init__(name)

        self.hud_field = []
        self.set_text(self.name)

        self.update_methods += [
            self.update_text
        ]

    def set_hud_field(self, target, attribute, default=""):
        self.hud_field = target, attribute, default

    def update_text(self):
        if self.hud_field:
            text = getattr(*self.hud_field)

            if self.text != text:
                self.set_text(text)
