"""
Test script to work with the XML Python library

Documentation: https://docs.python.org/3/library/xml.etree.elementtree.html
"""

import xml.etree.ElementTree as ET
import os
import csv


def csv2dict(csv_filename):
    f = open(csv_filename, "r")
    reader = csv.DictReader(f)
    d = {"items": []}
    for row in reader:
        d["items"].append(row)
    return d


# Import test MusicXML

pieceName = "BWV853"
arrangements = [
    {"name": "bartok"},
    {"name": "bischoff"},
    {"name": "busoni"},
    {"name": "czerny"},
    {"name": "dejong"},
    {"name": "selva"},
    {"name": "morgan"},
    {"name": "sporck"},
    {"name": "wouters"},
]

test_file = os.path.join(pieceName, "diff", arrangements[0]["name"] + "_diff.musicxml")
test_csv = os.path.join(pieceName, "diff", arrangements[0]["name"] + "_diff.csv")

# collect all the ids of objects
id_dictionary = csv2dict(test_csv)["items"]

id_list = []
for item in id_dictionary:
    id_list.append(item["id"])

# Generating XML tree
tree = ET.parse(test_file)
root = tree.getroot()


def find_elements_by_id(tree, id_list):
    elements_list = []
    for el in root.iter():
        try:
            if el.attrib["id"] in id_list:
                elements_list.append(el)
        except KeyError:
            pass

    return elements_list


def color_elements_list(elements_list, color="#FF0000"):
    for el in elements_list:
        el.attrib["color"] = color

    return elements_list


elements_list = find_elements_by_id(tree, id_list)
elements_list = color_elements_list(elements_list)

output_filename = os.path.join(pieceName, "diff", "output.musicxml")
tree.write(output_filename)
