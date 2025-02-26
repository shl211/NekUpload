from NekUpload.utils import parsing
import pytest

def test_split_equals_expr():
    expr = "abc def = 1234    "
    lhs = "abc def"
    rhs = "1234"

    expr_lhs,expr_rhs = parsing.get_both_sides_of_equals(expr)

    assert expr_lhs == lhs
    assert expr_rhs == rhs

def test_resolve_expr_no_eval():
    data = {"PARAM1": "10",
            "PARAM2" : "20"}
    expected = {"PARAM1": 10,
            "PARAM2" : 20}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_resolve_expr_sub_only():
    data = {"PARAM1": "10",
            "PARAM2" : "PARAM1"}
    expected = {"PARAM1": 10,
            "PARAM2" : 10}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_resolve_expr_sub_with_literal():
    data = {"PARAM1": "10",
            "PARAM2" : "PARAM1 + 5"}
    expected = {"PARAM1": 10,
            "PARAM2" : 15}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_resolve_expr_sub_with_var():
    data = {"PARAM1": "10",
            "PARAM2" : "2",
            "PARAM3" : "PARAM1 * PARAM2"}
    expected = {"PARAM1": 10,
            "PARAM2": 2,
            "PARAM3" : 20}
    
    result = parsing.evaluate_parameters(data)
    assert result == expected

def test_get_files_with_extension_normal():
    files = ["a.py","b.py","c.xml","d.xml","e.py"]
    files_py = ["a.py","b.py","e.py"]

    py = parsing.get_all_files_with_extension(files,".py")
    assert py == files_py

def test_get_files_with_extension_cases():
    files = ["a.py","b.py","c.xml","d.XML","e.py"]
    files_xml = ["c.xml","d.XML"]

    xml = parsing.get_all_files_with_extension(files,".xml")
    assert xml == files_xml

def test_get_files_with_extension_missing_dot_extension():
    files = ["a.py","b.py","c.xml","d.XML","e.py"]
    files_xml = ["c.xml","d.XML"]

    xml = parsing.get_all_files_with_extension(files,"xml")
    assert xml == files_xml

def test_get_files_with_extension_missing_dot_extension():
    files = ["a.py","b.py","c.xml","d.XML","e.py"]
    files_rst = []

    rst = parsing.get_all_files_with_extension(files,".rst")
    assert rst == files_rst