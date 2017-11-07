from src.context import Context
from src.game import start
from zs_globals import Settings

class_dict = {}
# class_dict = {cls.__name__: cls for cls in (
#     IMPORTED CLASSES HERE
# )}

# context = Context(class_dict, *IMPORTED INTERFACES HERE)
context = Context(class_dict)

start(
    Settings.APP_START, context
).main()

