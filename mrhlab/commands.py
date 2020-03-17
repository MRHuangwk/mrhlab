import click
from mrhlab.extensions import db

def register_commands(app):
    @app.cli.command()
    def init():
        from mrhlab.fakes import fake_admin, fake_categories, fake_applications
        db.drop_all()
        db.create_all()

        click.echo('Generating the admin...')
        fake_admin()

        click.echo('Generating categories...')
        fake_categories()

        click.echo('Generating applications...')
        fake_applications()

        click.echo('Done.')