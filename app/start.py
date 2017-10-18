from game import start
from app.sprites.text_sprite import TextSprite
from app.sprites.animation_sprite import AnimationSprite
from zs_globals import Settings


cd = {cls.__name__: cls for cls in (
    TextSprite,
    AnimationSprite
)}

start(
    Settings.APP_START,
    class_dict=cd
)
