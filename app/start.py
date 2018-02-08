from src.context import Context
from src.game import start
from zs_globals import Settings
from app.get_classes import get_all_classes

entities, interfaces = get_all_classes()

class_dict = {
    cls.__name__: cls for cls in entities
}
context = Context(class_dict, *interfaces)

start(
    Settings.APP_START, context
).main()

