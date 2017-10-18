from src.graphics import AnimationGraphics
from src.entities import Sprite


class AnimationSprite(Sprite):
    def __init__(self, name):
        super(AnimationSprite, self).__init__(name)

        self.animation = ""
        self.animation_state = ""

    def set_animation(self, file_name):
        self.animation = file_name
        self.graphics = AnimationGraphics.load_from_cfg(self, file_name)

    def set_animation_state(self, state_name):
        self.animation_state = state_name
        self.graphics.set_animation_state(state_name)
