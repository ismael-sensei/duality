import dotenv
import click
from app import bot

dotenv.load_dotenv()

@click.group()
def cli():
    pass

@cli.command()
def ping():
    click.echo('pong!')

@cli.command()
def discord():
    bot.run()