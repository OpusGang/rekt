from setuptools import setup

setup(name='rekt',
      version='r30',
      description='VapourSynth wrapper for Cropping and Stacking clips.',
      long_description='README.md',
      url='https://gitlab.com/Ututu/rekt',
      author='Ututu',
      author_email='daoko@protonmail.com',
      install_requires=['vapoursynth'],
      packages=['rekt'],
      zip_safe=False)