from app.interfaces.controller_interface import ControllerInterface
from app.interfaces.gui_interface import GuiInterface

from app.sprites.animation_sprite import AnimationSprite
from app.sprites.hud_sprite import HudSprite
from app.sprites.gui_sprites import BlockSprite, TextSprite
from game import start
from zs_globals import Settings

class_dict = {cls.__name__: cls for cls in (
    TextSprite,
    AnimationSprite,
    HudSprite,
    BlockSprite
)}

game = start(
    Settings.APP_START,
    class_dict,
    ControllerInterface,
    GuiInterface
).main()

