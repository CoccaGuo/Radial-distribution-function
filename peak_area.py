# peak_area.py by CoccaGuo at 2022/07/24 16:16

from matplotlib import pyplot as plt
import numpy as np
from path_utils import *

from rich.console import Console
from rich.table import Table

c = Console()

def one_gaussian(x, cen1, amp1, sigma1):
    return amp1*(1/(sigma1*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-cen1)/sigma1)**2)))


def adjust_fit(name):
    path = name2fit(name)
    if not os.path.exists(path):
        print('{} does not exist. run `fit` first.'.format(path))
        return
    data = np.loadtxt(path, delimiter=',', unpack=True)
    path = name2rdf(name)
    if not os.path.exists(path):
        print('{} does not exist. run `rdf` first.'.format(path))
        return
    r, rdf = np.loadtxt(path, delimiter=',', unpack=True)
    plot_peaks(name)
    ind = int(input('Which gaussian peak do you want to adjust? \n> '))
    print('Current parameters:', data[ind, 1:])
    inp = input('New parameters(split with commas,)\n> ')
    new_params = inp.split(',')
    data[ind, 1] = float(new_params[0])
    data[ind, 2] = float(new_params[1])
    data[ind, 3] = float(new_params[2])
    print('Current parameters:', data[ind, 1:], 'is this OK?(y/n)')
    if input('> ') == 'y':
        np.savetxt(name2fit(name), data.T, delimiter=',')
        print('{} is updated.'.format(path))
        plot_peaks(name)
    else:
        print('Aborted.')


def plot_peaks(name):
    path = name2rdf(name)
    if not os.path.exists(path):
        print('{} does not exist. run `rdf` first.'.format(path))
        return
    r, rdf = np.loadtxt(path, delimiter=',', unpack=True)
    plt.plot(r, rdf, 'ro', label='RDF', markersize=2)
    plt.xlabel('r/(nm)')
    plt.ylabel('RDF')
    path = name2fit(name)
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
    if os.path.exists(path):
        data = np.loadtxt(path, delimiter=',')
        ys = np.zeros(len(r))
        for i in range(data.shape[1]):
            yy = one_gaussian(r, *data[1:, i])
            ys += yy
            plt.plot(r, yy, label='gauss {}'.format(i), color=colors[i])
            plt.fill_between(r, yy.min(), yy, facecolor=colors[i], alpha=0.5)
        plt.plot(r, ys, label='sum', color='k')
    plt.legend()
    plt.title(name)
    plt.show()

    print('Is this Ok?(y/n)')
    if input('> ') == 'y':
        np.savetxt(name2fit(name), data, delimiter=',')
        print('{} is updated.'.format(path))
    else:
        print('Aborted.')


def origin(name):
    path = name2rdf(name)
    if not os.path.exists(path):
        print('{} does not exist. run `rdf` first.'.format(path))
        return
    print('Paste Origin Pro data format here: (format: xc, w, A)')
    data_list = []
    for i in range(3):
        inp = input('> ')
        if inp == 'q':
            return
        else:
            data_list.append([float(i.split(" ")[0]) for i in inp.split("\t")])
    data = np.array(data_list)
    
    data[[1,2], :] = data[[2,1], :]

    data = np.insert(data, 0, np.arange(data.shape[1]), axis=0)

    # print it on screen use rich table
    table = Table(title=f'{name} origin fit')
    table.add_column("Peak Index", justify="center", no_wrap=True)
    table.add_column('Center', justify='center', style='cyan')
    table.add_column('Amplitude', justify='center', style='cyan')
    table.add_column('Sigma', justify='center', style='cyan')

    for i in range(data.shape[1]):
        table.add_row(str(data[0, i]), str(data[1, i]), str(data[2, i]), str(data[3, i]))

    c.print(table)

    r, rdf = np.loadtxt(path, delimiter=',', unpack=True)
    plt.plot(r, rdf, 'ro', label='RDF', markersize=2)
    plt.xlabel('r/(nm)')
    plt.ylabel('RDF')
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
    ys = np.zeros(len(r))
    for i in range(data.shape[1]):
            yy = one_gaussian(r, *data[1:, i])
            ys += yy
            plt.plot(r, yy, label='gauss {}'.format(i), color=colors[i])
            plt.fill_between(r, yy.min(), yy, facecolor=colors[i], alpha=0.5)
    plt.plot(r, ys, label='sum', color='k')
    plt.legend()
    plt.title(name)
    plt.show()



def area(name):
    fit_path = name2fit(name)
    if not os.path.exists(fit_path):
        print('{} does not exist. run `fit` first.'.format(fit_path))
        return
    data = np.loadtxt(fit_path, delimiter=',')
    r = np.arange(0, 1.505, 0.005)
    area_data = np.zeros((6, data.shape[1]))
    for i in range(data.shape[1]):
        yy = one_gaussian(r, *data[1:, i])
        area = np.trapz(yy, r, dx=0.005)
        FWHM = 0.5887*data[3, i]  # the half width at half maximum
        center = data[1, i]
        r_p = np.arange(center-FWHM, center+FWHM, 0.005)
        yy_p = one_gaussian(r_p, *data[1:, i])
        partial_area = np.trapz(yy_p, r_p, dx=0.005)
        height = np.sqrt(2/np.pi)*data[2, i]/data[3, i]
        area_data[0, i] = i
        area_data[1, i] = center
        area_data[2, i] = FWHM
        area_data[3, i] = height
        area_data[4, i] = area
        area_data[5, i] = partial_area
    np.savetxt(name2area(name), area_data, delimiter=',')
    print('{} is saved.\n'.format(name2area(name)))
    table = Table(title='Area of Peaks')
    table.add_column("Index", justify="center", no_wrap=True)
    table.add_column("Peak Center", justify="center", no_wrap=True)
    table.add_column("FWHM*", justify="center", no_wrap=True)
    table.add_column("Peak Height", justify="center", no_wrap=True)
    table.add_column("Full Area", justify="center", no_wrap=True)
    table.add_column("FWHM Area", justify="center", no_wrap=True)

    for i in range(area_data.shape[1]):
        table.add_row(f"{area_data[0, i]:.0f}", f"{area_data[1, i]*1000:.1f} pm", f"{area_data[2, i]:.2f}",
                     f"{area_data[3, i]:.2f}", f"{area_data[4, i]*1000:.1f}", f"{area_data[5, i]*1000:.1f}")

    c.print(table)
    c.print("[italic green]* FWHM is the Full-Width at the Half of the Maximum.")
    
