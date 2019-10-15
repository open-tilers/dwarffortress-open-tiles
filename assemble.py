#!/bin/python3
import glob
import os
import sys

from PIL import Image


def get_configs():    
    config_files = glob.glob("config/*.TXT")

    configs = {}
    for config_file in config_files:
        config = os.path.splitext(os.path.basename(config_file).lower())[0]
        configs[config] = read_config_file(config_file)
    return configs


def read_config_file(config_file):
    with open(config_file, 'r') as cf:
        config_tiles = [config_tile.strip("[]\n").split(':', 2) for config_tile in cf.readlines()]

    tile_config = {config_tile[0]: config_tile[1] for config_tile in config_tiles}
    return tile_config
    


def get_assembled_image(config, tiles):
    assembled_image = Image.new('RGB', (2880, 2880))

    for y in range(16):
        for x in range(16):
            idx = x+(y*16)
            tile_file = tiles[f'TILE_{idx}']
            image = Image.open(f'input/{tile_file}')
            assembled_image.paste(image, (180*x,180*y))
    return assembled_image


configs = get_configs()
for config, tiles in configs.items():
    assembled_image = get_assembled_image(config, tiles)

    assembled_image.save(f'output/{config}.png')