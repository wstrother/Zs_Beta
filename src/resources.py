from os import listdir
from os.path import join

import pygame                           # PYGAME CHOKE POINT

from src.cfg import load_cfg, load_json
from zs_globals import Resources as Res
from zs_globals import Cfg

IMAGES = join(*Res.IMAGES)
SOUNDS = join(*Res.SOUNDS)
STYLES = join(*Res.STYLES)


def get_path(directory, file_name):
    """
    Search for a file in a given directory and its subdirectories
    """
    names = [f for f in listdir(directory) if f[0] not in "._"]
    files = [n for n in names if "." in n]
    dirs = [n for n in names if n not in files]

    if file_name in files:
        return join(directory, file_name)

    else:
        for d in dirs:
            try:
                return get_path(
                    join(directory, d), file_name)

            except FileNotFoundError:
                pass

        raise FileNotFoundError(join(directory, file_name))


def load_resource(file_name, section=None):
    """
    Search for and load a resource file as an object by searching
        resource directories using file extension as context
        for file path
    The section argument can be used to return a single section
        from a .cfg file
    File_names with no extension will automatically look for a
        .cfg file
    Passing None, False, or "" as the file_name will automatically
        return the PROJECT_CFG file specified in zs_globals.py
    """
    if not file_name:
        file_name = Cfg.PROJECT_CFG

    if "." not in file_name:
        file_name = file_name + "." + Res.CFG

    if section:
        try:
            return load_resource(file_name)[section]

        except KeyError:
            raise ValueError(
                "No '{}' section found in {}".format(
                    section, file_name
                )
            )

    else:
        ext = file_name.split(".")[-1]
        # print(file_name, ext)
        if ext == Res.CFG:
            path = get_path(Res.CFG, file_name)

        elif ext == Res.JSON:
            path = get_path(Res.JSON, file_name)

        elif ext in Res.IMAGE_EXT:
            path = get_path(IMAGES, file_name)

        elif ext in Res.SOUND_EXT:
            path = get_path(SOUNDS, file_name)

        else:
            path = get_path(Res.CFG, file_name)

    return get_object(ext, path)


def get_object(ext, path):
    """
    Contextually initializes an object for a given resource based on
      the file extension of the resource being loaded
    """
    if ext == Res.CFG:
        return load_cfg(path)

    if ext == Res.JSON:
        return load_json(path)

    if ext in Res.IMAGE_EXT:
        return pygame.image.load(path)              # PYGAME CHOKE POINT

    # if ext in Res.SOUND_EXT:
    #     return pygame.mixer.Sound(path)             # PYGAME CHOKE POINT

    else:
        file = open(path, "r")
        text = file.read()
        file.close()

        return text


def get_font(name, size, bold, italic):
    # PYGAME CHOKE POINT

    path = pygame.font.match_font(name, bold, italic)
    font = pygame.font.Font(path, size)

    return font
