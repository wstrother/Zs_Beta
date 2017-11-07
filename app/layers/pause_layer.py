from src.entities import Layer
from app.sprites.gui_sprites import BlockSprite


class PauseLayer(Layer):
    def __init__(self, name):
        super(PauseLayer, self).__init__(name)

        self.paused = True
        self.visible = False

        self.pause_target_layers = []

        self.cfg = {
            "groups": "Menu Group"
        }
        self.gui_interface = {
            "get_pause_menu": True
        }

    def get_pause_menu_data(self):
        pause_menu_json = {
            "class": "PauseMenuBlock",
            "controller": [self.name, 0],
            "position": [50, 50],
            "group": self.groups[0]
        }

        return pause_menu_json

    def set_pause_target_layers(self, *layers):
        for l in layers:
            self.add_to_list(
                "pause_target_layers", l
            )

    def on_pause(self):
        super(PauseLayer, self).on_pause()
        self.visible = not self.paused

        for l in self.pause_target_layers:
            l.handle_event("pause")


class PauseMenuBlock(BlockSprite):
    def __init__(self, name):
        super(PauseMenuBlock, self).__init__(name)

        self.gui_interface = {
            "get_menu_from_entity": "Demo Sprite",
            "add_return_option": "Main Menu"
        }
