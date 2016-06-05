import os
import ConfigParser

import click
import requests

USERNAME = None
TOKEN = None
API_BASE = 'https://bo.gg'


def create_config():
    config = ConfigParser.RawConfigParser()
    config.add_section('auth')
    config.set('auth', 'username', USERNAME)
    config.set('auth', 'token', TOKEN)

    with open('bogg.cfg', 'wb') as configfile:
        config.write(configfile)

def read_config():
    global USERNAME
    global TOKEN
    if not os.path.exists('bogg.cfg'):
        return
    config = ConfigParser.RawConfigParser()
    config.read('bogg.cfg')
    USERNAME = config.get('auth', 'username')
    TOKEN = config.get('auth', 'token')


def retrieve_token(password):
    global TOKEN
    payload = { 'username': USERNAME, 'password': password }
    response = requests.post(
        '{}/api/token-auth/'.format(API_BASE),
        json=payload,
    )
    response.raise_for_status()
    TOKEN = response.json()['token']
    create_config()

read_config()
