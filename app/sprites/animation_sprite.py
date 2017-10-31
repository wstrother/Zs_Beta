from src.graphics import AnimationGraphics
from src.entities import Sprite
from src.resources import load_resource


class AnimationSprite(Sprite):
    def __init__(self, name):
        super(AnimationSprite, self).__init__(name)

        self.animation = ""
        self.animation_state = ""

    def get_menu(self):
        menu = [
            [{"name": self.name, "selectable": False}],

            [
                {
                    "name": "Change Animation",
                    "on_activate": ["cycle_animation", self]
                },
                {
                    "name": "Animation State",
                    "hud_field": [self, "animation_state"],
                    "selectable": False
                }
            ],

            [
                {
                    "name": "Move Sprite",
                    "on_activate": ["toggle_movement", self],
                    "listeners": [
                        {
                            "name": "activate",
                            "target": "menu",
                            "response": "pause_pointer"
                        }
                    ]
                },
                None
            ]
        ]

        self.pause_event_method("move")

        return menu

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

    def toggle_movement(self):
        self.pause_event_method('move')

    def cycle_animation(self):
        names = self.get_animation_states()
        current = self.animation_state
        i = names.index(current)
        i += 1
        i %= len(names)
        self.set_animation_state(names[i])

    def on_move(self):
        event = self.event
        dx, dy = event['value']
        speed = event.get('speed', 1)
        self.move(dx, dy, v=speed)

    def on_cycle_animation(self):
        names = self.get_animation_states()
        current = self.animation_state
        i = names.index(current)
        i += 1
        i %= len(names)
        self.set_animation_state(names[i])
