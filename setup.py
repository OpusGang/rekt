from setuptools import setup

setup(
    name='rekt',
    version='1.0.0',
    description='VapourSynth wrapper for Cropping and Stacking clips.',
    long_description='README.md',
    url='https://github.com/OpusGang/rekt',
    author='OpusGang',
    packages=['rekt'],
    install_requires=[
        'VapourSynth>=57',
        'vsutil @ git+https://github.com/Irrational-Encoding-Wizardry/vsutil.git@956fa579406ca9edf6e0b6a834defae28efb51ce'
    ],
    zip_safe=False
)
