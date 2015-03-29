from distutils.core import setup

setup(
    name='Raspberry-Pi-IO',
    version='0.0.1',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    packages=['raspberry_pi_io'],
    url='https://github.com/exitcodezero/raspberry-pi-io',
    license='LICENSE.txt',
    description='A Python service for remotely controlling GPIO.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pika == 0.9.14",
    ],
)
