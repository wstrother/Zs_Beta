from src.entities import Sprite
from zs_globals import Events


class TestSprite(Sprite):
    def __init__(self, name):
        super(TestSprite, self).__init__(name)

        self.events_handled = []
        self.methods_called = []
        self.handle_event = self.log_event

    def log_event(self, event):
        event = self.event_handler.interpret(event)
        self.event_handler.handle_event(event)
        self.events_handled.append(
            event[Events.NAME]
        )

    def on_spawn(self):
        self.methods_called.append("on_spawn")

    def on_hear_spawn(self):
        self.methods_called.append("on_hear_spawn")

    def on_live(self):
        self.methods_called.append("on_live")

    def on_die(self):
        self.methods_called.append("on_die")


def event_test(p=False):
    t = TestSprite("bob")
    t.handle_event("spawn")

    spawned = "on_spawn" in t.methods_called

    if spawned and p:
        print("{} has spawned".format(t))

    assert spawned


def listener_test(p=False):
    t = TestSprite("bob")
    t.add_listener("spawn hear_spawn")
    t.handle_event("spawn")

    spawned = "on_spawn" in t.methods_called

    if spawned and p:
        print("{} has spawned".format(t))

    t.update()
    spawn_heard = "on_hear_spawn" in t.methods_called

    if spawn_heard and p:
        print("{} has heard the spawn event".format(t))

    assert t.listening_for("spawn")
    assert spawn_heard

    t.remove_listener("spawn", "hear_spawn")

    removed = not t.listening_for("spawn")

    if removed and p:
        print("{} has removed the spawn listener".format(t))

    assert removed


def chain_test(p=False):
    t = TestSprite("bob")
    make_event = t.event_handler.make_event
    life = 10

    events = [
        "spawn",
        make_event("live", duration=life),
        "die"
    ]

    t.queue_event(*events)

    t.update()

    spawned = "on_spawn" in t.methods_called
    if spawned and p:
        print("{} has spawned".format(t))
    assert spawned

    for i in range(life):
        t.update()

        lived = "on_live" == t.methods_called[-1]
        if lived and p:
            print("{} has lived".format(t))
        assert lived

    t.update()
    dead = "on_die" in t.methods_called
    if dead and p:
        print("{} has died".format(t))
    assert dead
