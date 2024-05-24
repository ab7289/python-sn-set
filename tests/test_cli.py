from os import path
from unittest import mock

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


@mock.patch("sn_set.cli.to_excel")
@mock.patch("sn_set.cli.get_set_diff")
@mock.patch("sn_set.cli.get_install_order_new")
@mock.patch("sn_set.cli.get_install_order")
@mock.patch("sn_set.cli.get_update_sets")
def test_cli_valid(
    mock_get_update_sets,
    mock_get_install_order,
    mock_new_install_order,
    mock_set_diff,
    mock_to_excel,
    runner,
):
    mock_set1 = [
        {"name": "a set", "sys_id": "12345"},
        {"name": "b set", "sys_id": "54321"},
    ]
    mock_set2 = [{"name": "a set", "sys_id": "54321"}]
    mock_install_order = [{"name": "b set", "sys_id": "12345"}]

    mock_get_update_sets.side_effect = [mock_set1, mock_set2]
    mock_get_install_order.return_value = mock_install_order
    mock_set_diff.side_effect = [["b set"], []]
    mock_to_excel.return_value = True

    test_source = "nyudev"
    test_target = "nyuqa"
    result = runner.invoke(cli.main, ["--source", test_source, "--target", test_target])

    mock_get_update_sets.assert_any_call("nyudev")
    mock_get_update_sets.assert_any_call("nyuqa")
    mock_set_diff.assert_has_calls(
        [
            mock.call(["a set", "b set"], ["a set"], debug=False),
            mock.call(["b set"], ["b set"]),
        ]
    )
    mock_new_install_order.assert_not_called()
    mock_to_excel.assert_called_once_with(mock_install_order, None)

    assert result.exit_code == 0
    assert not result.exception
    assert (
        f"Begin retrieving update sets from "
        f"source: {test_source} and target: {test_target}"
    ) in result.output
    assert "Success" in result.output


@mock.patch("sn_set.cli.to_excel")
@mock.patch("sn_set.cli.get_set_diff")
@mock.patch("sn_set.cli.get_install_order_new")
@mock.patch("sn_set.cli.get_install_order")
@mock.patch("sn_set.cli.get_update_sets")
def test_cli_valid_with_new(
    mock_get_update_sets,
    mock_get_install_order,
    mock_new_install_order,
    mock_set_diff,
    mock_to_excel,
    runner,
):
    mock_set1 = [
        {"name": "a set", "sys_id": "12345"},
        {"name": "b set", "sys_id": "54321"},
        {"name": "c set", "sys_id": "0987"},
    ]
    mock_set2 = [{"name": "a set", "sys_id": "12345"}]
    mock_install_order = [{"name": "b set", "sys_id": "12345"}]
    mock_final_install_order = [
        {"name": "b set", "sys_id": "12345"},
        {"name": "c set", "sys_id": "0987"},
    ]

    mock_get_update_sets.side_effect = [mock_set1, mock_set2]
    mock_get_install_order.return_value = mock_install_order
    mock_set_diff.side_effect = [["b set", "c set"], ["c set"]]
    mock_new_install_order.return_value = [{"name": "c set", "sys_id": "0987"}]
    mock_to_excel.return_value = True

    test_source = "nyudev"
    test_target = "nyuqa"
    result = runner.invoke(cli.main, ["--source", test_source, "--target", test_target])

    mock_get_update_sets.assert_any_call("nyudev")
    mock_get_update_sets.assert_any_call("nyuqa")
    mock_set_diff.assert_has_calls(
        [
            mock.call(["a set", "b set", "c set"], ["a set"], debug=False),
            mock.call(["b set", "c set"], ["b set"]),
        ]
    )
    # mock_set_diff.assert_any_call(["a set", "b set", "c set"], ["a set"], debug=False)
    mock_new_install_order.assert_called_with("nyudev", ["c set"])
    mock_to_excel.assert_called_once_with(mock_final_install_order, None)

    assert result.exit_code == 0
    assert not result.exception
    assert (
        f"Begin retrieving update sets from "
        f"source: {test_source} and target: {test_target}"
    ) in result.output
    assert "Success" in result.output


@mock.patch("sn_set.cli.to_excel")
@mock.patch("sn_set.cli.get_set_diff")
@mock.patch("sn_set.cli.get_install_order_new")
@mock.patch("sn_set.cli.get_install_order")
@mock.patch("sn_set.cli.get_update_sets")
def test_cli_valid_with_file(
    mock_get_update_sets,
    mock_get_install_order,
    mock_new_install_order,
    mock_set_diff,
    mock_to_excel,
    runner,
):
    mock_set1 = [
        {"name": "a set", "sys_id": "12345"},
        {"name": "b set", "sys_id": "54321"},
        {"name": "c set", "sys_id": "0987"},
    ]
    mock_set2 = [{"name": "a set", "sys_id": "12345"}]
    mock_install_order = [{"name": "b set", "sys_id": "12345"}]
    mock_final_install_order = [
        {"name": "b set", "sys_id": "12345"},
        {"name": "c set", "sys_id": "0987"},
    ]

    mock_get_update_sets.side_effect = [mock_set1, mock_set2]
    mock_get_install_order.return_value = mock_install_order
    mock_set_diff.side_effect = [["b set", "c set"], ["c set"]]
    mock_new_install_order.return_value = [{"name": "c set", "sys_id": "0987"}]
    mock_to_excel.return_value = True

    test_source = "nyudev"
    test_target = "nyuqa"
    test_file = "nyudev_order"
    result = runner.invoke(
        cli.main,
        ["--source", test_source, "--target", test_target, "-f", test_file, "--debug"],
    )

    mock_get_update_sets.assert_any_call("nyudev")
    mock_get_update_sets.assert_any_call("nyuqa")
    mock_set_diff.assert_has_calls(
        [
            mock.call(["a set", "b set", "c set"], ["a set"], debug=True),
            mock.call(["b set", "c set"], ["b set"]),
        ]
    )
    mock_new_install_order.assert_called_with("nyudev", ["c set"])
    mock_to_excel.assert_called_once_with(mock_final_install_order, test_file)

    assert result.exit_code == 0
    assert not result.exception
    assert (
        f"Begin retrieving update sets from "
        f"source: {test_source} and target: {test_target}"
    ) in result.output
    assert "Success" in result.output


@mock.patch("sn_set.cli.to_excel")
@mock.patch("sn_set.cli.get_set_diff")
@mock.patch("sn_set.cli.get_install_order_new")
@mock.patch("sn_set.cli.get_install_order")
@mock.patch("sn_set.cli.get_update_sets")
def test_cli_valid_with_failed_excel(
    mock_get_update_sets,
    mock_get_install_order,
    mock_new_install_order,
    mock_set_diff,
    mock_to_excel,
    runner,
):
    mock_set1 = [
        {"name": "a set", "sys_id": "12345"},
        {"name": "b set", "sys_id": "54321"},
        {"name": "c set", "sys_id": "0987"},
    ]
    mock_set2 = [{"name": "a set", "sys_id": "12345"}]
    mock_install_order = [{"name": "b set", "sys_id": "12345"}]
    mock_final_install_order = [
        {"name": "b set", "sys_id": "12345"},
        {"name": "c set", "sys_id": "0987"},
    ]

    mock_get_update_sets.side_effect = [mock_set1, mock_set2]
    mock_get_install_order.return_value = mock_install_order
    mock_set_diff.side_effect = [["b set", "c set"], ["c set"]]
    mock_new_install_order.return_value = [{"name": "c set", "sys_id": "0987"}]
    mock_to_excel.return_value = False

    test_source = "nyudev"
    test_target = "nyuqa"
    result = runner.invoke(cli.main, ["--source", test_source, "--target", test_target])

    mock_get_update_sets.assert_any_call("nyudev")
    mock_get_update_sets.assert_any_call("nyuqa")
    mock_set_diff.assert_any_call(["a set", "b set", "c set"], ["a set"], debug=False)
    mock_set_diff.assert_any_call(["a set", "b set", "c set"], ["a set"], debug=False)
    mock_new_install_order.assert_called_with("nyudev", ["c set"])
    mock_to_excel.assert_called_once_with(mock_final_install_order, None)

    assert result.exit_code == -1
    assert result.exception
    assert (
        f"Begin retrieving update sets from "
        f"source: {test_source} and target: {test_target}"
    ) in result.output
    assert "There was an error writing the spreadsheet" in result.output


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
        (["cat", "dog", "fish"], ["cat", "dog"], ["fish"]),
        (["cat", "dog"], ["dog", "fish"], ["cat"]),
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
        {"name": "set3", "sys_id": {"display_value": "a value"}},
    ]
    with runner.isolated_filesystem():
        cli.to_excel(test_set_list, test_value)

        assert path.exists(expected_value) is True


@pytest.mark.parametrize("test_value", [None, {}, [], 1])
def test_to_excel_invalid(test_value):
    assert cli.to_excel(test_value, None) is False
