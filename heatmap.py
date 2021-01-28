import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from PIL import Image

#if packages are needed use command $pip3 install <package>
#Example: pip3 install pandas

#to create visualization for all csv files in the directory, run $python3 heatmap.py
#to run script for a specific file run $python heatmap.py <data file>.csv

# n_skip_rows = 5   #accumulative number of rows to skip
# user_file = sys.argv[1]
# user_ID = user_file[5:12]
directory = os.fsencode("/Users/kzayas/exploration/Naturalistic_Exploration/PHP")

def create_plot(user_file, skip_rows):
    # print(skip_rows)
    user_ID = user_file[5:12]
    cols = list(pd.read_csv(user_file, skiprows=skip_rows, nrows=1))
    stimuli = cols[0].replace(" Time","")
    print(stimuli)

    if stimuli == "Answer" or stimuli == "Comment":
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
    plt.close()

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

def create_multi_pdf(user_file):
    img_list = []
    user_ID = user_file[5:12]
    n_skip_rows = 5     #accumulative number of rows to skip

    while True:
        returned_value = create_plot(user_file, n_skip_rows)

        if returned_value == "Answer":
            n_skip_rows += 2
        elif returned_value == "Comment":
            break
        else:
            img_list.append(returned_value)
            n_skip_rows += 8

    img = img_list[0]
    img.save(user_ID +'.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=img_list[1:]) #combine into 1 pdf


# print(len(sys.argv))
if len(sys.argv) == 2:
    user_file = sys.argv[1]
    create_multi_pdf(user_file)
else:
    for file in os.listdir(directory):
         filename = os.fsdecode(file)
         if filename.endswith("csv"):
             print(filename)
             create_multi_pdf(filename)
         else:
             continue
