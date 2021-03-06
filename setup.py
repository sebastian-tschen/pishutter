from setuptools import setup

setup(
    name='PiShutter',
    version='0.1',
    packages=['shutter', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=[
        'flask',
        'RPi.GPIO'
    ],

)
