import click
from app import bot
from adapter.presenter.cli.other_cli_presenter import OtherCLIPresenter
from domain.use_cases.other_use_case import OtherUseCase
import asyncio

@click.group()
def cli():
    pass

@cli.command()
def ping():
    asyncio.run(OtherUseCase(OtherCLIPresenter()).ping())

@cli.command()
def discord():
    bot.run()