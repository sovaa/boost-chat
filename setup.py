from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='boostchat',
    version=version,
    description="Scalable websocket chat server",
    long_description="""\
""",
    classifiers=[],
    keywords='chat',
    author='Oscar Eriksson',
    author_email='oscar.eriks@gmail.com',
    license='GPLv3',
    package_data={},
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'flask-socketio==2.7.1',
        'flask_wtf',
        'wtforms',
        'redis',
    ],
    entry_points={
        'console_scripts': [
            'boostchat = boostchat:entry',
        ],
    }
)
