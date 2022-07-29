# interactive.py by CoccaGuo at 2022/07/13 10:55
import base64
import json
import math
import sys

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def get_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    pts = list(map(lambda shape: (shape['points'][0]), data['shapes']))
    imageHeight = data['imageHeight']
    imageWidth = data['imageWidth']
    return pts, (imageHeight, imageWidth), data['imageData'], data['imagePath']


def save_img(imgstr):
    img = base64.b64decode(imgstr)
    img_name_ = "image.png"
    with open(img_name_, 'wb') as jpg_file:
        jpg_file.write(img)
    

def open_img():
    return plt.imread("image.png")


def inter(file_name, s_b):
    image_scale_bar = float(s_b)

    pts, size, imgstr, imgName = get_data(file_name)
    pix2real = image_scale_bar/size[0]
    real2pix = size[0]/image_scale_bar

    save_img(imgstr)
    img = open_img()

    r_init = 480

    def ring(r):
        return r / 1000 * real2pix

    # Create the figure and the line that we will manipulate
    plt.imshow(img)
    circle = plt.Circle(pts[0], ring(r_init), color='r', fill=False)
    circle1 = plt.Circle(pts[0], ring(r_init), color='r', fill=False)
    plt.gcf().gca().add_artist(circle)
    plt.gcf().gca().add_artist(circle1)

    # plot points
    p_x, p_y = zip(*pts)
    plt.scatter(p_x, p_y, s=1, c='b')

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(bottom=0.25)

    # Make a horizontal slider to control the frequency.
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
    freq_slider = Slider(
        ax=axfreq,
        label='Radius (pm)',
        valmin=0,
        valmax=1500,
        valinit=r_init,
    )

    axamp = plt.axes([0.1, 0.25, 0.0225, 0.63])
    amp_slider = Slider(
    ax=axamp,
    label='Radius (pm)',
    valmin=0,
    valmax=1500,
    valinit=r_init,
    orientation="vertical"
)

    def update1(val):
        r = amp_slider.val
        circle1.set_radius(ring(r))

    def update(val):
        r = freq_slider.val
        circle.set_radius(ring(r))
    
    freq_slider.on_changed(update)
    amp_slider.on_changed(update1)


    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, 'Select', hovercolor='0.975')

    def find_point(event):
        plt.title('click to select point')
        # wait for user to click on the plot
        user_pt = plt.ginput(1)[0]
        # find the closest point
        min_dist = sys.maxsize
        min_pt = None
        for pt in pts:
            dist = distance(pt, user_pt)
            if dist < min_dist:
                min_dist = dist
                min_pt = pt
        # update the circle
        circle.center = min_pt
        circle1.center = min_pt
        # redraw the circle
        plt.draw()
        plt.title('')
    
    button.on_clicked(find_point)
        

    plt.show()
