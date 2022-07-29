# polt.py by CoccaGuo at 2022/07/23 17:36

from matplotlib import gridspec
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from rich.console import Console
from rich.table import Table

from ser_dat import *

def fit(name):
    rdf_file = name2rdf(name)
    x, data = np.loadtxt(rdf_file, delimiter=',', unpack=True)


    def one_gaussian(x, cen1, amp1, sigma1):
        return amp1*(1/(sigma1*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-cen1)/sigma1)**2)))

    def two_gaussians(x, c1, amp1, sigma1, c2, amp2, sigma2):
        return amp1*(1/(sigma1*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-c1)/sigma1)**2))) + \
                amp2*(1/(sigma2*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-c2)/sigma2)**2)))
            
    def three_gaussians(x, c1, amp1, sigma1, c2, amp2, sigma2, c3, amp3, sigma3):
        return amp1*(1/(sigma1*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-c1)/sigma1)**2))) + \
                amp2*(1/(sigma2*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-c2)/sigma2)**2))) + \
                amp3*(1/(sigma3*(np.sqrt(np.pi/2))))*(np.exp((-2.0)*(((x-c3)/sigma3)**2)))


    # section 1 --> 1/2 gaussians
    border = data[105:140]
    border_index = np.argmin(border) + 105
    x_s1 = x[:border_index]
    data_s1 = data[:border_index]

    # section 2 --> 2/3
    border2 = data[200:230]
    border_index2 = np.argmin(border2) + 200
    x_s2 = x[border_index:border_index2]
    data_s2 = data[border_index:border_index2]

    # section 3 --> 2
    x_s3 = x[border_index2:]
    data_s3 = data[border_index2:]

    # section 1 guess
    guess_s1_1 = [0.475, 0.32, 0.1]
    guess_s1_2 = [0.325, 0.06, 0.1, 
                0.475, 0.32, 0.1,]

    # section 2 guess
    guess_s2_2 = [0.690, 0.17, 0.1,
                0.936, 0.14, 0.1]

    guess_s2_3 = [0.690, 0.13, 0.1,
                0.830, 0.10, 0.1,
                0.940, 0.20, 0.1]

    # section 3 guess 
    guess_s3_2 = [1.200, 0.22, 0.1,
                1.440, 0.22, 0.1]

    # show section dist
    fig, axe = plt.subplots(1, 1, figsize=(10,8))
    axe.plot(x_s1, data_s1, 'b', label='section 1')
    axe.plot(x_s2, data_s2, 'r', label='section 2')
    axe.plot(x_s3, data_s3, 'g', label='section 3')
    axe.legend()
    axe.set_title('Section distribution')
    plt.show()


    # section 1 fit
    # 1.1
    popt_gauss_1_1, pcov_gauss_1_1 = optimize.curve_fit(one_gaussian, x_s1, data_s1, p0=guess_s1_1)
    gauss_peak_1_1 = one_gaussian(x_s1, *popt_gauss_1_1)


    fig = plt.figure(figsize=(8,4))
    gs = gridspec.GridSpec(1,2)
    ax1 = fig.add_subplot(gs[0])


    ax1.plot(x_s1, gauss_peak_1_1, color='b', label='fit A')
    ax1.fill_between(x_s1, gauss_peak_1_1.min(), gauss_peak_1_1, facecolor='b', alpha=0.5)
    ax1.plot(x_s1, data_s1, "ro", markersize=2)
    ax1.set_title('A')
    ax1.legend()

    # 1.2
    popt_gauss_1_2, pcov_gauss_1_2 = optimize.curve_fit(two_gaussians, x_s1, data_s1, p0=guess_s1_2)
    gauss_peak_1_2 = two_gaussians(x_s1, *popt_gauss_1_2)

    ax2 = fig.add_subplot(gs[1])

    pars_1_2_1 = popt_gauss_1_2[0:3]
    pars_1_2_2 = popt_gauss_1_2[3:6]
    gauss_peak_1_2_1 = one_gaussian(x_s1, *pars_1_2_1)
    gauss_peak_1_2_2 = one_gaussian(x_s1, *pars_1_2_2)

    # peak 1
    ax2.plot(x_s1, gauss_peak_1_2_1, "g")
    ax2.fill_between(x_s1, gauss_peak_1_2_1.min(), gauss_peak_1_2_1, facecolor="green", alpha=0.5)
    
    # peak 2
    ax2.plot(x_s1, gauss_peak_1_2_2, "y")
    ax2.fill_between(x_s1, gauss_peak_1_2_1.min(), gauss_peak_1_2_2, facecolor="yellow", alpha=0.5) 
    ax2.plot(x_s1, gauss_peak_1_2, color='b', label='fit B')
    ax2.plot(x_s1, data_s1, "ro", markersize=2, label='rdf data')
    ax2.set_title('B')
    ax2.legend()

    plt.suptitle("Section 1: Which is better?")

    plt.show()

    area_data = {}
    area_data['s1'] = []
    area_data['s2'] = []
    area_data['s3'] = []

    result = input("Which Is Better? (a/b):\n> ")
    if result == 'a' or result == 'A':
        area_data['s1'].append(popt_gauss_1_1)
    elif result == 'b' or result == 'B':
        area_data['s1'].append(pars_1_2_1)
        area_data['s1'].append(pars_1_2_2)

    # section 2 fit
        # 2.1
    popt_gauss_2_1, pcov_gauss_2_1 = optimize.curve_fit(two_gaussians, x_s2, data_s2, p0=guess_s2_2)
    gauss_peak_2_1 = two_gaussians(x_s2, *popt_gauss_2_1)

    fig = plt.figure(figsize=(8,4))
    gs = gridspec.GridSpec(1,2)
    ax1 = fig.add_subplot(gs[0])

    pars_2_1_1 = popt_gauss_2_1[0:3]
    pars_2_1_2 = popt_gauss_2_1[3:6]
    gauss_peak_2_1_1 = one_gaussian(x_s2, *pars_2_1_1)
    gauss_peak_2_1_2 = one_gaussian(x_s2, *pars_2_1_2)

    # peak 1
    ax1.plot(x_s2, gauss_peak_2_1_1, "g")
    ax1.fill_between(x_s2, gauss_peak_2_1_1.min(), gauss_peak_2_1_1, facecolor="green", alpha=0.5)
    
    # peak 2
    ax1.plot(x_s2, gauss_peak_2_1_2, "y")
    ax1.fill_between(x_s2, gauss_peak_2_1_2.min(), gauss_peak_2_1_2, facecolor="yellow", alpha=0.5) 
    ax1.plot(x_s2, gauss_peak_2_1, color='b', label='fit A')
    ax1.plot(x_s2, data_s2, "ro", markersize=2, label='rdf data')
    ax1.set_title('A')
    ax1.legend()

        # 2.2
    popt_gauss_2_2, pcov_gauss_2_2 = optimize.curve_fit(three_gaussians, x_s2, data_s2, p0=guess_s2_3)
    gauss_peak_2_2 = three_gaussians(x_s2, *popt_gauss_2_2)
    ax2 = fig.add_subplot(gs[1])

    pars_2_2_1 = popt_gauss_2_2[0:3]
    pars_2_2_2 = popt_gauss_2_2[3:6]
    pars_2_2_3 = popt_gauss_2_2[6:9]

    gauss_peak_2_2_1 = one_gaussian(x_s2, *pars_2_2_1)
    gauss_peak_2_2_2 = one_gaussian(x_s2, *pars_2_2_2)
    gauss_peak_2_2_3 = one_gaussian(x_s2, *pars_2_2_3)

        # peak 1
    ax2.plot(x_s2, gauss_peak_2_2_1, "g")
    ax2.fill_between(x_s2, gauss_peak_2_2_1.min(), gauss_peak_2_2_1, facecolor="green", alpha=0.5)

        # peak 2
    ax2.plot(x_s2, gauss_peak_2_2_2, "y")
    ax2.fill_between(x_s2, gauss_peak_2_2_2.min(), gauss_peak_2_2_2, facecolor="yellow", alpha=0.5)

        # peak 3
    ax2.plot(x_s2, gauss_peak_2_2_3, "r")
    ax2.fill_between(x_s2, gauss_peak_2_2_3.min(), gauss_peak_2_2_3, facecolor="red", alpha=0.5)
    ax2.plot(x_s2, gauss_peak_2_2, color='b', label='fit B')
    ax2.plot(x_s2, data_s2, "ro", markersize=2)
    ax2.set_title('B')
    ax2.legend()

    plt.suptitle("Section 2: Which is better?")
    plt.show()

    result = input("Which Is Better? (a/b):\n> ")
    if result == 'a' or result == 'A':
        area_data['s2'].append(pars_2_1_1)
        area_data['s2'].append(pars_2_1_2)
    elif result == 'b' or result == 'B':
        area_data['s2'].append(pars_2_2_1)
        area_data['s2'].append(pars_2_2_2)
        area_data['s2'].append(pars_2_2_3)

        # section 3 fit
        # 3.1
    popt_gauss_3_1, pcov_gauss_3_1 = optimize.curve_fit(two_gaussians, x_s3, data_s3, p0=guess_s3_2)
    gauss_peak_3_1 = two_gaussians(x_s3, *popt_gauss_3_1)

    pars_3_1_1 = popt_gauss_3_1[0:3]
    pars_3_1_2 = popt_gauss_3_1[3:6]

    gauss_peak_3_1_1 = one_gaussian(x_s3, *pars_3_1_1)
    gauss_peak_3_1_2 = one_gaussian(x_s3, *pars_3_1_2)

    fig = plt.figure(figsize=(4,4))
    gs = gridspec.GridSpec(1,1)
    ax1 = fig.add_subplot(gs[0])

        # peak 1
    ax1.plot(x_s3, gauss_peak_3_1_1, "g")
    ax1.fill_between(x_s3, gauss_peak_3_1_1.min(), gauss_peak_3_1_1, facecolor="green", alpha=0.5)

        # peak 2
    ax1.plot(x_s3, gauss_peak_3_1_2, "y")
    ax1.fill_between(x_s3, gauss_peak_3_1_2.min(), gauss_peak_3_1_2, facecolor="yellow", alpha=0.5)
    ax1.plot(x_s3, gauss_peak_3_1, color='b', label='fit A')
    ax1.plot(x_s3, data_s3, "ro", markersize=2, label='rdf data')
    ax1.set_title('Check')
    ax1.legend()

    plt.suptitle("Section 3")
    plt.show()

    area_data['s3'].append(pars_3_1_1)
    area_data['s3'].append(pars_3_1_2)

    peaks = []
    for ss, it in area_data.items():
        peaks.extend(it)

    console = Console()
    table = Table(title="Fit Report")
    table.add_column("Peak Index", justify="center", no_wrap=True)
    table.add_column("Center", justify="center", no_wrap=True)
    table.add_column("Amplitude", justify="center", no_wrap=True)
    table.add_column("Sigma", justify="center", no_wrap=True)


    for i, it in enumerate(peaks):
        table.add_row(str(i), str(it[0]), str(it[1]), str(it[2]))

    console.print(table)
    console.print("[red bold]Please carefully check the center and sigma information above.")
    # console.print("[green]The Amplitude is not important, because only range information is used to calculate the area size.")   
    console.print("if you are not satisfied with the result, you can upgrade the data manually.")

    plt.plot(x, data, "ro", markersize=2)

    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']

    # plot this peaks
    for i, it in enumerate(peaks):
        plt.plot(x, one_gaussian(x, *it), label=str(i), color=colors[i])
        plt.fill_between(x, one_gaussian(x, *it).min(), one_gaussian(x, *it), facecolor=colors[i], alpha=0.5)
    plt.legend()
    plt.title("Peaks Report")
    plt.show()

    output_data = np.zeros((len(peaks), 4))
    for i, it in enumerate(peaks):
        output_data[i, 0] = i
        output_data[i, 1] = it[0]
        output_data[i, 2] = it[1]
        output_data[i, 3] = it[2]

    # save the data as csv
    fit_path = name2fit(name)
    np.savetxt(fit_path, output_data.T, delimiter=",")
    console.print("[green]The fit result has been saved to {}".format(fit_path))



