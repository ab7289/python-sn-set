from os import path

import pytest

from sn_set import cli


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code != 0
    assert result.exception


def test_cli_no_source(runner):
    result = runner.invoke(cli.main, ["--target", "nyudev"])
    assert result.exit_code != 0
    assert result.exception


def test_cli_no_target(runner):
    result = runner.invoke(cli.main, ["--source", "nyudev"])
    assert result.exit_code != 0
    assert result.exception


# def test_cli_valid(runner, monkeypatch):
#     mock_sets = [
#         {
#             'name': 'a set',
#             'sys_id': '12345'
#         },
#         {
#             'name': 'b set',
#             'sys_id': '54321'
#         }
#     ]

#     def mock_get_update_sets(instance_name):
#         return mock_sets

#     monkeypatch.setattr(cli, "get_update_sets", mock_get_update_sets)
#     monkeypatch.setattr(cli, "get_install_order", mock_get_update_sets)

#     test_source = "nyudev"
#     test_target = "nyuqa"
#     result = runner.invoke(cli.main,
#       ["--source", test_source, "--target", test_target])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert (
#         f"Begin retrieving update sets from "
#         f"source: {test_source} and target: {test_target}"
#     ) in result.output


@pytest.mark.parametrize(
    "test_value1,test_value2,expected_value",
    [
        (["one", "two", "three"], ["two", "three"], ["one"]),
        ("fish", ["cat"], "error"),
        (["fish"], "cat", "error"),
        (None, ["fish"], "error"),
        (["fish"], None, "error"),
        ([None, "fish"], ["cat"], "error"),
        (["cat", "fish"], ["fish", 1], "error"),
        (["Cat", " doG ", "fish"], ["cat", "dog"], ["fish"]),
    ],
)
def test_set_diff_values(test_value1, test_value2, expected_value):
    if expected_value == "error":
        with pytest.raises(ValueError):
            cli.get_set_diff(test_value1, test_value2)
    else:
        assert cli.get_set_diff(test_value1, test_value2) == expected_value


@pytest.mark.parametrize(
    "test_value,expected_value",
    [(None, "output.xlsx"), ("test_file_name", "test_file_name.xlsx")],
)
def test_to_excel_valid(test_value, expected_value, runner):
    test_set_list = [
        {"name": "set1", "sys_id": "12345"},
        {"name": "set2", "sys_id": "54321"},
    ]
    with runner.isolated_filesystem():
        if test_value:
            cli.to_excel(test_set_list, file=test_value)
        else:
            cli.to_excel(test_set_list)

        assert path.exists(expected_value) is True


@pytest.mark.parametrize("test_value", [None, {}, [], 1])
def test_to_excel_invalid(test_value):
    assert cli.to_excel(test_value) is False
