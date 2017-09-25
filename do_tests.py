import tests.cfg_tests as cfg
import tests.context_tests as context
import tests.events_test as event
from sys import argv

PRINT_TESTS = False

tests = [
    cfg.cfg_json_test,
    cfg.check_syntax_test,
    cfg.value_type_test,
    context.serialize_test,
    event.event_test,
    event.listener_test,
    event.chain_test
]

names = [t.__name__ for t in tests]
test_dict = dict(zip(names, tests))


def do_test(m):
    n = m.__name__
    print("\n-----\nRUNNING {}".format(n))
    if PRINT_TESTS:
        print("")
    m(p=PRINT_TESTS)
    print("\n{}: OK\n-----\n\n".format(n))


if __name__ == "__main__":
    if "print" in argv:
        PRINT_TESTS = True
        argv.pop(argv.index("print"))

    if len(argv) > 1:
        names = [
            n + "_test" for n in argv[1:] if n + "_test" in test_dict
        ]

    for name in names:
        do_test(test_dict[name])
