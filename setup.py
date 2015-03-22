from setuptools import setup

setup(
    name='grindy',
    version='0.1',
    packages=['grindy', 'grindy.rating', 'grindy.tools'],
    url='https://github.com/Granitas/Grindy',
    license='GPL',
    author='Granitas',
    author_email='bernardas.alisauskas@gmail.com',
    description='Grindy is a command line application for long term memory(LTM) training. Application uses user crea'
                'ted decks with question & answers to question the user using rating algorithms and other LTM methods.',
    install_requires=[
        "colorama",
    ],
    package_data={'': ['decks/*', 'LICENSE', 'README.md']},
    package_dir={'grindy': 'grindy'},
    include_pacakage_data=True,
)
