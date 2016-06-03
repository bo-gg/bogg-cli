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

       bogg sunset-jog             (Log my sunset jog, which I've pre-defined in my lookups)

    """
    if not calories:
        interactive()
        return

    if calories.isdigit():
        calories = int(calories)
    else:
        raise NotImplementedError('Lookups aren\'t done yet.')

    create_entry(calories, note, ate)


def setup():
    pass

def log():
    pass

def add_shortcut(calories, note):
    pass


def create_measurement(weight):
    raise NotImplementedError('Weight measurement not implemented.')

def create_entry(calories, note, ate=True, dt_occurred=None):
    if not ate:
        calories = calories * -1
    if not dt_occurred:
        dt_occurred = datetime.datetime.now()

    payload = {
        'entry_type': 'C' if ate else 'E',
        'calories': calories,
        'note': note,
        'dt_occurred': str(dt_occurred)
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
        print payload
        print response.content
        print response
        exit()

    click.echo(click.style('Logged {} calories.'.format(calories), fg='green'))
    show_status()

def show_status():
    date_string = datetime.date.today()
    response = requests.get(
        'http://localhost:8000/api/daily/{}'.format(date_string),
        auth=('admin', 'changeme'),
    )
    data = response.json()
    click.echo(' - You have eaten {} calories.'.format(data['calories_consumed']))
    click.echo(' - You have burned off {} calories.'.format(abs(data['calories_expended'])))
    if data['calories_remaining'] > 0:
        message = 'You can eat {} more calories today.'.format(data['calories_remaining'])
        click.echo(
            click.style(message, fg='green')
        )
    elif data['calories_remaining'] < 0:
        message = 'You have exceeded your goal by {} calories.'.format(abs(data['calories_remaining']))
        click.echo(
            click.style(message, fg='red')
        )
    else:
        message = 'You are exactly at your calorie goal.'
        click.echo(
            click.style(message, fg='green')
        )

def show_log():
    response = requests.get(
        'http://localhost:8000/api/daily/',
        auth=('admin', 'changeme'),
    )
    data = response.json()['results']
    for entry in data:
        ''' "date": "2016-05-11",
        "calories_consumed": 100,
        "calories_expended": 0,
        "net_calories": 100,
        "calories_remaining": null
        '''
        click.echo('{}: {} eaten, {} exercised, {} remaining.'.format(
            entry['date'],
            entry['calories_consumed'],
            entry['calories_expended'],
            entry['calories_remaining'],
        ))


def interactive():
    click.echo('1: Log calories eaten.')
    click.echo('2: Log calories exercised.')
    click.echo('3: Record a new weight measurement.')
    click.echo('4: Log an item from your quick-lookups.')
    click.echo('5: Add an item to your quick-lookups.')
    click.echo('6: View status for today.')
    click.echo('7: View a log of the past few days.')
    click.echo('8: Edit configuration.')
    click.echo('Command? ', nl=False)
    while True:
        c = click.getchar()
        if c.isdigit():
            break
        click.echo('Invalid option.')

    click.echo()
    c = int(c)
    if c == 1 or c == 2:
        ate = c == 1
        calories = click.prompt('Number of calories', type=int)
        action = "eat" if ate else "do"
        note = click.prompt('What did you {}?'.format(action))
        create_entry(calories, note, ate)
    elif c == 3:
        weight = click.prompt('Enter your new weight', type=int)
        create_entry(weight)
    elif c == 4:
        #TODO: Lookup items via pager
        pass
    elif c == 5:
        click.echo('(F)ood or (E)xercise? ')
        c = click.getchar().lower()
        ate = c == 'F'
        calories = click.prompt('Number of calories', type=int)
        note = click.prompt('Name this entry')
        create_entry(calories, note, ate)
        add_shortcut(calories, note)
    elif c == 6:
        show_status()
    elif c == 7:
        show_log()
    elif c == 8:
        #TODO: Edit page for config
        pass
