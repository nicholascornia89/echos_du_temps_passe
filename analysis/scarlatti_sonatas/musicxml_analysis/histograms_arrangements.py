"""Histogram visualization of data in PieceFolder"""

import matplotlib.pyplot as plt
import numpy as np
import csv, json
import os
import pandas as pd


# FUNCTIONS
def import_json_file(fn):
    # Import json file
    with open(fn, "r") as f:
        json_file = json.load(f)
        # print(json_file)
        return json_file


def colorByGroupHistogram(objects, values, value_label, colors):
    fig, ax = plt.subplots()

    bar_labels = objects
    bar_colors = colors
    ax.bar(objects, values, label=bar_labels, color=bar_colors)

    ax.set_ylabel("value")
    ax.set_title("Arrangement Analysis")
    ax.legend(title=value_label)
    plt.tight_layout()
    plt.rcParams.update({"figure.autolayout": True})
    plt.style.use("fast")
    plt.savefig(os.path.join(base_path, "statistics_" + value_label + ".png"), dpi=600)


base_path = "./K9"
arrangements = []
for file in os.listdir(base_path):
    # check extension
    if os.path.splitext(file)[1] == ".json":
        # load json file as dictionary
        arrangements.append(
            {
                "name": file.split("_")[0].capitalize(),
                "statistics": import_json_file(os.path.join(base_path, file)),
            }
        )

# set colors
colors = []
for arrangement in arrangements:
    colors.append((np.random.random(), np.random.random(), np.random.random()))

for key in arrangements[0]["statistics"].keys():
    objects = []
    values = []
    for arrangement in arrangements:
        objects.append(arrangement["name"])
        values.append(arrangement["statistics"][key])

    colorByGroupHistogram(objects, values, key, colors)
