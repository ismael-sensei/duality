import pytest
from click.testing import CliRunner
from app import cli



def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['ping'])
    assert result.exit_code == 0
    assert 'pong!' in result.output