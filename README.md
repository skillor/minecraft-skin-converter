# Minecraft Skin Converter
This is a simplified version of https://github.com/811Alex/MCSkinConverter, ported to python.
Big Thanks to the original creator [811Alex](https://github.com/811Alex)

Convert skins from alex to steve and vice versa.

## Installation

> pip install minecraft-skin-converter

## Basic Usage
```python
from minecraft_skin_converter import SkinConverter

sc = SkinConverter()
sc.load_from_file('steve.png')
print(sc.is_steve())
sc.steve_to_alex()
sc.save_to_file('steve_as_alex.png')
```