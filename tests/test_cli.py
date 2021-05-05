from sn_set import cli


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception
    assert "Entrypoint for the program" in result.output.strip()
