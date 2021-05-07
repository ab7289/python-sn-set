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


def test_cli_valid(runner):
    test_source = "nyudev"
    test_target = "nyuqa"
    result = runner.invoke(cli.main, ["--source", test_source, "--target", test_target])
    assert result.exit_code == 0
    assert not result.exception
    assert (
        f"Begin retrieving update sets from "
        f"source: {test_source} and target: {test_target}"
    ) in result.output


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
    ],
)
def test_set_diff_values(test_value1, test_value2, expected_value):
    if expected_value == "error":
        with pytest.raises(ValueError):
            cli.get_set_diff(test_value1, test_value2)
    else:
        assert cli.get_set_diff(test_value1, test_value2) == expected_value
