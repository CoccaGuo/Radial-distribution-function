# ser_dat.py by CoccaGuo at 2022/07/23 14:06

import os
from rdf_core import calc
from path_utils import *


def rdf_calc(name, force=False, ref_length=1.5):
    if not force:
        if os.path.exists(name2rdf(name)):
            print('{} already exists. Use -f to force re-calculate.'.format(name2rdf(name)))
            return
    file = name2struct(name)
    save_path = name2rdf(name)
    calc(file, ref_length, save_path)
    print('{} is calculated.'.format(save_path))

            

