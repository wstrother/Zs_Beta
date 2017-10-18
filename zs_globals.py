class Zs:
    PRINT_CFG_LOG = False

# =======================
# CFG Keywords / Settings
# =======================


class Cfg:
    # global project cfg data

    PROJECT_CFG = "zs.cfg"

    # section names

    GROUPS = "groups"
    LAYERS = "layers"
    POPULATE = "populate"

    # items in these sections will be initialized by context.py

    CONSTRUCTOR_SECTIONS = (LAYERS,)

    # items in these sections will be initialized in order

    ORDERED_SECTIONS = (POPULATE,)

    # value keywords

    FALSE_KEYWORD = "false"
    TRUE_KEYWORD = "true"
    NONE_KEYWORD = "null"
    MODEL = "model"

    # parameter keywords

    ADD_TO_MODEL = "add_to_model"
    CLASS_KEYWORD = "class"
    PARENT_LAYER = "parent_layer"

    # special reserved keywords

    INIT_KEYS = (           # special keys that should be
        ADD_TO_MODEL,       # ignored by the init_item() method
        CLASS_KEYWORD,
        PARENT_LAYER)


# ===========================
# Project Directories / Files
# ===========================

class Resources:
    CFG = "cfg"
    ENVIRONMENTS = CFG, "environments"
    JSON = "json"

    RESOURCES = "resources"
    IMAGES = RESOURCES, "images"
    SOUNDS = RESOURCES, "sounds"
    STYLES = RESOURCES, "styles"

    IMAGE_EXT = "gif", "png", "jpg", "svg", "bmp", "ico"
    SOUND_EXT = ".wav", ".mp3", ".ogg", ".flac"


# =============
# Game Settings
# =============

class Settings:
    SCREEN_SIZE = 1100, 600
    FRAME_RATE = 60


# ===============
# Event Dict Keys
# ===============

class Events:
    """
    event = {
        NAME: str,
        TEMP: bool=True,
        TIMER: Timer(DURATION),
        DURATION: int=1,
        LERP: bool=True,
        LINK: event=None,
        TRIGGER: event=None
    }

    listener = {
        NAME: str,
        TEMP: bool=True,
        TARGET: Entity()=self.entity,
        RESPONSE: event
    }
    """
    NAME = "name"
    TEMP = "temp"
    TIMER = "timer"
    DURATION = "duration"
    LERP = "lerp"
    LINK = "link"
    TARGET = "target"
    RESPONSE = "response"
    TRIGGER = "trigger"


class ControllerInputs:
    CONTROLLER_FRAME_DEPTH = 300
    INIT_DELAY = 30
    HELD_DELAY = 15
    UDLR = "up", "down", "left", "right"
    AXES = "x_axis", "y_axis"
    STICK_DEAD_ZONE = .1
    AXIS_MIN = .9
