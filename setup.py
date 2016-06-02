from setuptools import setup

setup(
    name='bogg',
    version='0.1',
    py_modules=['bogg'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        bogg=cli:cli
        bogg-interactive=cli:interactive
        bogg-add-entry=cli:add_entry
    ''',
)
