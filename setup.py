#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [x for x in fh.read().splitlines() if x]

setup(name='Minecraft Skin Converter',
      packages=['minecraft_skin_converter'],
      version='1.2',
      description='Convert minecraft skins from steve to alex and vice versa',
      author='skillor',
      author_email='skillor@gmx.net',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      url='https://github.com/skillor/minecraft-skin-converter',
      keywords=['minecraft', 'skin-converter', 'minecraft_skin_converter', 'minecraft-skin-converter'],
      classifiers=['Programming Language :: Python :: 3 :: Only',
                   'Topic :: Multimedia :: Graphics'],
      setup_requires=["wheel"],
      install_requires=requirements,
      python_requires='>=3',
      )
