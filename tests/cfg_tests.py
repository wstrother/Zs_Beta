from os.path import join

from src.cfg import save_cfg, save_json, check_cfg_syntax, get_cfg
from src.resources import load_resource


def cfg_json_test(p=False):
    example_file = "test_example"
    example_text = """# tables

Hello World
\ta_description: "Hi, It's an example of CFG data syntax for ZSquirrel"
\tb_test_value: 1.3
\tc_test_list: 1, 2, 3, 4
\td_single_element_list: "one",
"""

    ex = get_cfg(check_cfg_syntax(example_text))

    save_json(ex, join("json", example_file + ".json"))
    ex_js = load_resource(example_file + ".json")
    save_cfg(ex_js, join("cfg",  example_file + ".cfg"))

    for name in ex["tables"]:
        table = ex["tables"][name]
        json_table = ex_js["tables"][name]

        for key in table:
            if p:
                print("comparison...")
                print("\tCFG:", table[key])
                print("\tJSON:", json_table[key])

            assert table[key] == json_table[key]


def check_syntax_test(p=False):
    examples = ["""#section_name

table
\tvalue
    """, """#

table
\tvalue
    #""", """# section_name

 table
\tvalue""", """# section_name

table
\tvalue:
"""]

    missed_errors = False

    for e in examples:
        try:
            assert check_cfg_syntax(e, warning=False)
            missed_errors = True

        except ValueError as e:
            if p:
                print("Syntax error caught:\n\t{}".format(e))

    assert not missed_errors


def value_type_test(p=False):
    example = """# tables

Hello World
\tinteger: 1
\tstring1: "Hey, this isn't not a string"
\tstring2: another string here
\tlist: 1, 2, meow
\tfloat: 3.01
\tsingle_element_list: hello,
\tbool_false: false
\tbool_true
"""

    ex = get_cfg(example)
    hw = ex["tables"]["Hello World"]

    value_types = {
        "integer": int,
        "string1": str,
        "string2": str,
        "list": [int, int, str],
        "float": float,
        "single_element_list": [str],
        "bool_false": bool,
        "bool_true": bool
    }

    for key in hw:
        value = hw[key]
        vt = value_types[key]

        if p:
            print(value, type(value), vt)

        if not type(value) is list:
            assert type(value) is vt

        else:
            assert all(
                [type(item) is vt[value.index(item)] for item in value]
            )
