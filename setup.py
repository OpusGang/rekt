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
        'vsutil==0.7.0',
    ],
    zip_safe=False
)
