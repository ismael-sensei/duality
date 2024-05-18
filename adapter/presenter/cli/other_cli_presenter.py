from domain.interfaces.output import OtherOutput
import click

class OtherCLIPresenter(OtherOutput):
    async def pong(self):
        click.echo('pong!')