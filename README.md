# Minecraft Skin Converter

[![Build Status](https://github.com/skillor/minecraft-skin-converter/actions/workflows/test-python.yml/badge.svg)](https://github.com/skillor/minecraft-skin-converter/actions/workflows/test-python.yml) [![PyPi version](https://badgen.net/pypi/v/minecraft-skin-converter/)](https://pypi.org/project/minecraft-skin-converter)

This is a simplified version of https://github.com/811Alex/MCSkinConverter, ported to python.
Big Thanks to the original creator [811Alex](https://github.com/811Alex)

Convert skins from alex to steve and vice versa.

## Installation

```bash
pip install minecraft-skin-converter
```

## Basic Usage
```python
from minecraft_skin_converter import SkinConverter

sc = SkinConverter()
sc.load_from_file('steve.png')
print(sc.is_steve())
sc.steve_to_alex()
sc.save_to_file('steve_as_alex.png')
```
