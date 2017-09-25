from src.cfg import get_cfg
from src.context import set_environment_context
from src.entities import Layer, Environment, Sprite
from src.resources import load_resource


def serialize_test(p=False):
    env_name = "Demo Environment"
    file_name = "Demo_Environment.cfg"
    move_x, move_y = 200, 100
    example_text = """
# populate


Test Sprite
\tadd_to_model
\tclass: Sprite
\tsize: 50, 50
\tposition: 100, 100
\tgroup: Sprite Group


# groups


Sprite Group


# layers


Sprite Layer
\tclass: Layer
\tgroups: Sprite Group


"""

    try:
        cfg = load_resource(file_name)
    except FileNotFoundError:
        cfg = get_cfg(example_text)

    cd = {
        "Layer": Layer,
        "Environment": Environment,
        "Sprite": Sprite
    }

    env = Environment(env_name)
    if p:
        print("SETTING ENVIRONMENT CONTEXT")
    set_environment_context(env, cd, cfg, p=p)

    # move test sprite
    test_sprite = env.model["Test Sprite"]
    if p:
        print("MOVING {} ({}, {})\n".format(
            test_sprite, move_x, move_y
        ))

    old_x, old_y = test_sprite.position
    test_sprite.move(move_x, move_y)

    if p:
        print("SAVING ENVIRONMENT STATE AS CFG")
    env.save_state_as_cfg(p=p)

    new_cfg = load_resource(file_name)
    new_x, new_y = new_cfg["populate"]["Test Sprite"]["position"]

    assert (old_x + move_x, old_y + move_y) == (new_x, new_y)
