from src.graphics import AnimationGraphics
from src.entities import Sprite
from src.resources import load_resource


class AnimationSprite(Sprite):
    def __init__(self, name):
        super(AnimationSprite, self).__init__(name)

        self.animation = ""
        self.animation_state = ""

    def set_animation(self, file_name):
        self.animation = file_name
        cfg = load_resource(file_name, section="animations")
        self.graphics = AnimationGraphics.load_from_cfg(
            self, cfg
        )
        self.set_animation_state(
            cfg["info"].get("default", "default")
        )

    def set_animation_state(self, state_name):
        self.animation_state = state_name
        self.graphics.set_animation_state(state_name)

    def get_animation_states(self):
        if self.graphics:
            return self.graphics.get_animation_states()
