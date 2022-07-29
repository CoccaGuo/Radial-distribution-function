from posixpath import dirname
import matplotlib.pyplot as plt
import numpy as np
from path_utils import name2rdf, path2name
import os

def plotting(*args):
    if len(args) == 0:
        dirname_ = os.path.dirname(name2rdf('foo.cocca'))
        all_rdf_data = os.listdir(dirname_)
        for rdf_file in all_rdf_data:
            if rdf_file.endswith('.csv'):
                file_p = os.path.join(dirname_, rdf_file)
                r, rdf = np.loadtxt(file_p, delimiter=',', unpack=True)
                plt.plot(r, rdf, label=path2name(rdf_file))
    else:
        for name in args:
            r, rdf = np.loadtxt(name2rdf(name), delimiter=',',unpack=True)
            plt.plot(r, rdf, label=name)
    plt.legend()
    plt.title('RDF analysis')
    plt.xlabel('r (nm)')
    plt.ylabel('rdf(r)')
    plt.show()
