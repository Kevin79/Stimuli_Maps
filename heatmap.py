import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from PIL import Image

n_skip_rows = 5   #accumulative number of rows to skip
user_file = sys.argv[1]
user_ID = user_file[5:12]

def create_plot(skip_rows):
    # print(skip_rows)
    cols = list(pd.read_csv(user_file, skiprows=skip_rows, nrows=1))
    stimuli = cols[0].replace(" Time","")
    # print(stimuli)

    if stimuli == "Answer" or stimuli == "Comments":
        return stimuli

    #transpose set of rows and delete empty entries
    data = pd.read_csv(user_file, skiprows=skip_rows, nrows=4, index_col = False, usecols =[i for i in cols if "Time" not in i]).T
    data.dropna(inplace=True)

    #create plot
    plt.figure()
    plt.scatter(data[1], data[2], s = 1, c=np.arange(len(data[1])))
    plt.axis('square')
    plt.ylim(-100, 100)
    plt.xlim(-100, 100)
    plt.savefig(user_ID +'.png',transparent=True)

    #open plot and crop
    plot = Image.open(user_ID +'.png')
    plot_width, plot_height = plot.size
    left = 143
    top = 58
    right = plot_width - 126
    bottom = plot_height - 52
    plot2 = plot.crop((left, top, right, bottom))
    plot2.save(user_ID +'.png',"PNG")

    # #open map and rezise plot to maps size
    map = Image.open("Stimuli_Maps/" + stimuli + ".png")
    map_width, map_height = map.size
    plot2 = plot2.resize((map_width, map_height),Image.ANTIALIAS)

    #overlay
    map.paste(plot2, (0, 0), plot2)
    map = map.convert('RGB')
    os.remove(user_ID +'.png')

    return map

img_list = []

while True:

    returned_value = create_plot(n_skip_rows)

    if returned_value == "Answer":
        n_skip_rows += 2
    elif returned_value == "Comment":
        break
    else:
        img_list.append(returned_value)
        n_skip_rows += 8

#combine into 1 pdf
img = img_list[0]
img.save(user_ID +'.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:])
