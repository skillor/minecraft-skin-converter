import sys

with open('setup_template.py', 'r', encoding='utf-8') as fr:
    with open('setup.py', 'w', encoding='utf-8') as fw:
        fw.write(fr.read().replace('{$MINECRAFT_SKIN_CONVERTER_VERSION}', sys.argv[1]))
