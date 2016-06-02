import click
import requests
import datetime

@click.command()
@click.option('--ate/--exercised', default=True, help="Ate or Exercised (default: Ate)")
@click.argument('calories', required=False)
@click.argument('note', required=False)
def cli(ate, calories, note):
    """Command line interface for bo.gg

    Examples:

       bogg 100                    (I ate 100 calories)

       bogg 300 sandwich           (I ate a 300-calorie sandwich)

       bogg --exercised 200 bike   (I rode my bike and worked off 200 calories)

    """
    if not calories:
        interactive()

    payload = {
        'entry_type': 'C' if ate else 'E',
        'calories': calories,
        'note': note,
        'dt_occurred': str(datetime.datetime.now())
    }
    if not note:
        payload['note'] = 'Command line entry with no note.'

    response = requests.post(
        'http://localhost:8000/api/entries/',
        auth=('admin', 'changeme'),
        json=payload,
    )

    try:
        response.raise_for_status()
    except:
        print response.content
        print response

    click.echo(click.style('Logged {} calories.'.format(calories), fg='green'))

    date_string = datetime.date.today()
    response = requests.get(
        'http://localhost:8000/api/daily/{}'.format(date_string),
        auth=('admin', 'changeme'),
    )
    data = response.json()
    click.echo(' - You have eaten {} calories.'.format(data['calories_consumed']))
    click.echo(' - You have exercised {} calories.'.format(data['calories_expended']))
    click.echo(' - You have {} calories remaining today.'.format(data['net_calories']))



def add_shortcut():
    pass

def interactive():
    click.echo('[a]te, [e]xercised, [q]uick-lookup? [a] ', nl=False)
    c = click.getchar().lower()
    click.echo()
    if c == 'a' or c == chr(13):
        click.echo('You ate')
    elif c == 'e':
        click.echo('Exercised')
    elif c == 'q':
        click.echo('Show food list')
    else:
        click.echo('Invalid input :(')
        click.echo(c)
        click.echo(ord(c))
    pass
