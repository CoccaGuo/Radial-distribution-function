# path_utils.py by CoccaGuo at 2022/07/24 15:30

import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)


def name2struct(name):
    p = '\\'.join(name.split(' '))
    return os.path.join(config['base'], 'data', p, 'struct.txt')


def struct2name(path):
    base_path = os.path.dirname(path)
    return ' '.join(base_path.split('data')[1].split('\\')[1:])


def name2rdf(name):
    p = '_'.join(name.split(' ')) + '-rdf.csv'
    return os.path.join(config['base'], config['output'], p)

def name2fit(name):
    p = '_'.join(name.split(' ')) + '-fit.csv'
    return os.path.join(config['base'], config['fit'], p)

def name2area(name):
    p = '_'.join(name.split(' ')) + '-area.csv'
    return os.path.join(config['base'], config['area'], p)

def path2name(path):
    return ' '.join(os.path.basename(path).split('.')[0].split('_'))

