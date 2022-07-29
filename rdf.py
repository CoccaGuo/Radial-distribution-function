# rdf.py by CoccaGuo at 2022/07/23 23:35
import json
import os
from rich.console import Console
from rich.table import Table
from ser_dat import rdf_calc
from polt import fit
from inter import inter
from path_utils import *
from peak_area import plot_peaks, adjust_fit, area, origin
from plotting import plotting

def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def walk_dir(dir):
    for root, _, files in os.walk(dir):
        for file in files:
            yield os.path.join(root, file)

def list_files(opt=None):
    base = cfg['base']
    labels = []
    for file in walk_dir(os.path.join(base, 'data')):
        if file.endswith('struct.txt'):
            infos = struct2name(file)
            labels.append(infos)
    if opt:
        console.print("List all available files:")
        for label in labels:
            console.print(label)
    return labels


def calc_rdf(flag=None):
    global cxt
    if cxt == '/':
        print('Please select a file first.')
        return
    force = False
    if flag == '-f':
        force = True
    rdf_calc(cxt, force=force, ref_length=cfg['RDF_ref_length'])


def calc_fit():
    global cxt
    if cxt == '/':
        print('Please select a file first.')
        return
    if not os.path.exists(name2rdf(cxt)):
        print('{}\'s rdf file does not exist. Please run \'rdf\' first.'.format(cxt))
        return
    if os.path.exists(name2fit(cxt)):
        print('{}\'s fit file already exists.'.format(cxt))
        return
    fit(cxt)

def list_stats():
    labels = list_files()
    table = Table(title="Current RDF Data Status")
    table.add_column("Name", justify="center", no_wrap=True)
    table.add_column("Condition", justify="center", no_wrap=True)
    table.add_column("RDF calc", justify="center", no_wrap=True)
    table.add_column("Fit calc", justify="center", no_wrap=True)
    table.add_column("Area calc", justify="center", no_wrap=True)

    for i, label in enumerate(labels):
        rdf = fit = area = '✗'
        if os.path.exists(name2rdf(label)):
                rdf = '✓'
        if os.path.exists(name2fit(label)):
                fit = '✓'
        if os.path.exists(name2area(label)):
                area = '✓'
        # other way to say is area calced.
        table.add_row(str(i),label, rdf, fit, area)
    
    console.print(table)

def select_item(index):
    labels = list_files()
    aim_label = labels[int(index)]
    global cxt
    cxt = aim_label

def quit_func():
    global cxt
    if cxt != '/':
        cxt = '/'
        return
    else:
        print('Bye!')
        exit(0) 

def interactive():
    global cxt
    if cxt == '/':
        print('Please select a file first.')
        return
    bp = os.path.dirname(name2struct(cxt))
    files = []
    scale_bars = []
    with open(name2struct(cxt), 'r') as f:
        line = f.readline()              
        while line:  
            lines = line.strip().split(' ')
            files.append(lines[0])
            scale_bars.append(float(lines[1]))
            line = f.readline()
    print('name', '\t', 'json name')
    print('_____________________')
    for i, file in enumerate(files):
        print(i, '\t' ,file)
    print('_____________________')
    print('Please select an area:')
    index = int(input())
    file = files[index]
    scale_bar = scale_bars[index]
    file = os.path.join(bp, file)
    inter(file, scale_bar)



def commands(cmd):
    if cmd == 'list' or cmd == 'ls':
        list_stats()
    elif cmd == 'stat':
        list_stats()
    elif cmd == 'clear' or cmd == 'cls' or cmd == 'clc':
        os.system('cls')
    elif cmd.startswith('sel') or cmd.startswith('cd') or cmd.startswith('use'):
        try:
            select_item(cmd.split(' ')[1])
        except:
            print('Please input a valid index.')
    elif cmd.startswith('rdf'):
        if ' ' in cmd:
            calc_rdf(cmd.split(' ')[1])
        else: 
            calc_rdf()
    elif cmd == 'fit':
        calc_fit()
    elif cmd == 'adjust':
        adjust_fit(cxt)
    elif cmd == 'origin':
        origin(cxt)
    elif cmd == 'area':
        area(cxt)
    elif cmd.startswith('inter'):
        interactive()
    elif cmd.startswith('show') or cmd.startswith('plot'):
        if cxt == '/':
            if len(cmd.split(' ')) > 1:
                lists = list_files()
                plotting(*[lists[int(ind)] for ind in cmd.split(' ')[1:]])
            else:
                plotting()
        else:
            plot_peaks(cxt)
    elif cmd == 'quit' or cmd =='exit' or cmd =='q' or cmd == 'bye':
        quit_func()
    else:
        try:
            exec(f"print({cmd})")
        except:
            try:
                exec(cmd)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    cfg = get_config()
    console = Console()
    cxt = '/'
    console.rule("[bold red]Welcome to RDF terminal.")
    console.rule("Copyright(c) 2022 CoccaGuo")
    while True:
        console.print(f'({cxt}) >> ', end='')
        cmd = input()
        if ';' in cmd:
            cmds = cmd.split(';')
            for cmd in cmds:
                commands(cmd.strip())
        else:
            commands(cmd)