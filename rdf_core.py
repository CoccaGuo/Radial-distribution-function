# rdf_core.py by CoccaGuo at 2022/07/23 14:15

# test.py by CoccaGuo at 2022/07/05 15:33
# output_data.py by CoccaGuo at 2022/07/12 13:21
# dist_calc.py by CoccaGuo at 2022/07/12 13:29
# copyright(c) 2022 CoccaGuo

# use this to calculate the RDF

import json
import os
import math
from itertools import combinations
import numpy as np

def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def stat_distance(points):
    _list = []
    for combinator in combinations(points, 2):
        _list.append(distance(*combinator))
    return sorted(_list)


def get_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    pts = list(map(lambda shape: (shape['points'][0]), data['shapes']))
    imageHeight = data['imageHeight']
    imageWidth = data['imageWidth']
    return pts, (imageHeight, imageWidth), data['imageData'], data['imagePath']



def overlap_sum(r, distance, r_ref, rho_circle, dr = 1):
    if r < distance - r_ref:
        return 0
    elif r > distance + r_ref:
        return 0
    else:
        theta = math.acos((r**2 + distance**2 - r_ref**2 )/(2*r*distance))
        arc = r * theta
        return arc * dr * rho_circle * 2


def single_dist_func(pts, size, index=0, center=None, step=1, stop=200):
    # get the reference radius
    count = len(pts)
    area = size[0] * size[1]
    ref_r = (0.06 * real2pix) # 0.2nm = 200pm 
    little_circle = math.pi*ref_r**2
    rho_circle = 1/little_circle
    rho = count / area
    pt = pts[index]
    if center:
        pt = center
    dist_list = list()
    local_rho_list = list()
    for _pt in pts:
        dist_list.append(distance(pt, _pt))
    list.sort(dist_list) # sort the distance list
    dist_list.pop(0) # remove the first element, itself
    for i in np.arange(0, stop+step, step):
        # local_count = len(
        #     list(filter(lambda x: x < i and x >= i-step, dist_list)))
        i = i*real2pix
        local_count = sum(map(lambda x: overlap_sum(i, x, ref_r, rho_circle, dr=step), dist_list))
        local_area = math.pi*(i**2-(i-step)**2)
        local_rho = local_count / local_area
        local_rho_list.append(local_rho/rho)
    return local_rho_list


def calc(struct_file, ref_length, save_path, force=False):
    files = list()
    scale_bars = list()
    base_path = os.path.dirname(struct_file)
    os.chdir(base_path)
    with open('struct.txt', 'r') as f:
        line = f.readline()
        while line:  
            lines = line.strip().split(' ')
            files.append(lines[0])
            scale_bars.append(float(lines[1]))
            line = f.readline()   
    RDF_x_axis_length = ref_length
    infos = '_'.join(base_path.split('data')[1].split('\\')[1:])
    print(f"Processing {infos}")

    step_ = 0.005 # in nm = 2pm
    stop_ = RDF_x_axis_length

    r_list = list(np.arange(0, stop_+step_, step_))
    total_dist_list = np.zeros(len(r_list))
    counter = 0

    for i, fi in enumerate(files):

        sorted_, size, imgstr, imgName = get_data(fi)

        # exchanger from pixel to real space
        global real2pix
        global pix2real
        pix2real = scale_bars[i]/size[0]
        real2pix = size[0]/scale_bars[i]

        # multi point start
        # get the center area points

        _stop_pix_ = int(stop_*real2pix) + 1

        center_zone = (_stop_pix_, size[0] - _stop_pix_,
                    _stop_pix_, size[1] - _stop_pix_)

        center_pts = list(filter(
            lambda x: center_zone[0] <= x[0] <= center_zone[1] and center_zone[2] <= x[1] <= center_zone[3], sorted_))

        r_list = np.array(r_list)
    

        for ind, center_pt in enumerate(center_pts):
            result_list = single_dist_func(
                sorted_, size, index=0, center=center_pt, step=step_, stop=stop_)
            total_dist_list += np.array(result_list)
        
        counter += len(center_pts)
    
    total_dist_list = total_dist_list/counter
    # multi point end

    # save the data with numpy format
    result_path = save_path
    np.savetxt(result_path, np.column_stack((r_list, total_dist_list)), delimiter=',')


    # load the data with numpy format
    # r_list, total_dist_list = np.loadtxt('RDF.csv', delimiter=',', unpack=True)

