from setuptools import setup

setup(
    name='vs-rekt',
    version='1.0.0',
    description='VapourSynth wrapper for Cropping and Stacking clips.',
    url='https://github.com/OpusGang/rekt',
    author='OpusGang',
    packages=['rekt'],
    license="MIT",
    install_requires=[
        'VapourSynth>=57',
        'vsutil>=0.7.0',
    ],
    zip_safe=False
)
