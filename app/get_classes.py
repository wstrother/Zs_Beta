import inspect
from os import listdir
from os.path import join
import importlib


def get_classes_from_module(module):
    return list(filter(
        lambda c: inspect.getmodule(c) is module,
        [c[1] for c in inspect.getmembers(module, inspect.isclass)]
    ))


def get_modules_from_directory(directory):
    path = join("app", directory)
    file_names = listdir(path)
    file_names = list(filter(
        lambda f: f not in ("__pycache__", "__init__.py"),
        file_names
    ))

    modules = []

    for file_name in file_names:
        file_name = "".join(file_name.split(".")[:-1])
        name = "app.{}.{}".format(directory, file_name)
        modules.append(importlib.import_module(name))

    return modules


def get_all_classes():
    entity_classes = []

    for directory in ("sprites", "layers"):
        modules = get_modules_from_directory(directory)

        for module in modules:
            entity_classes += get_classes_from_module(module)

    interface_classes = []

    for module in get_modules_from_directory("interfaces"):
        interface_classes += get_classes_from_module(module)

    return entity_classes, interface_classes

