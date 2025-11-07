""" 
Unified BWV 853 script

I am not concerned to voicing and layout, thus I a m flattening all voices into one

"""

import sys

sys.path.append(".")  # import utilities functions from model directory.

import os
import csv, json
import music21 as m21
from model import *


# Import MusicXML paths
transcriptionsPath = "../encoded_music/project_transcriptions/"
pieceName = "BWV853"
piecePath = os.path.join(transcriptionsPath, pieceName, "musicxml")
arrangements = [
    {"name": "durr", "year": 1989, "type": "urtext"},
    {"name": "czerny","year": 1830, "type": "arrangement"},  # 1830
    {"name": "bischoff","year": 1889, "type": "arrangement"},  # 1889
    {"name": "busoni","year": 1894, "type": "arrangement"},  # 1894
    {"name": "wouters","year": 1899, "type": "arrangement"},  # 1899
    {"name": "bartok","year": 1907, "type": "arrangement"},  # 1907
    {"name": "morgan","year": 1912, "type": "arrangement"},  # 1912
    {"name": "dejong","year": 1925, "type": "arrangement"},  # 1925
    {"name": "sporck","year": 1914, "type": "arrangement"},  # 1914
    {"name": "selva","year": 1915, "type": "arrangement"},  # 1915
]


# Generate Music21 scores
for a in arrangements:
    a["filename"] = os.path.join(piecePath, pieceName + "_" + a["name"] + ".musicxml")
    a["score"] = m21.converter.parse(a["filename"])


def musicxml_analysis():
    # Create subdirectories
    os.makedirs(pieceName, exist_ok=True)
    os.makedirs(os.path.join(pieceName,"csv"), exist_ok=True)
    # create corpus list
    corpus = []

    # Arrangements analysis
    for a in arrangements:
        print(f"Current edition: {a["name"]} ")
        arrangementDictionary, arrangementStatistics, a["score"] = m21stream2dict(
            a["score"], a["name"]
        )

        arrangementDictionary = sorted(
            arrangementDictionary, key=lambda x: x["measure_start"]
        )

        dict2csv(
            arrangementDictionary, os.path.join(pieceName, "csv", a["name"] + ".csv")
        )
        # json_file = open(os.path.join(pieceName, a["name"] + "_statistics.json"), "w")
        # json.dump(arrangementStatistics, json_file, indent=2)
        corpus.append({"metadata": {}, "statistics": {}})
        corpus[-1]["statistics"] = arrangementStatistics
        corpus[-1]["metadata"] = {
            "type": a["type"],
            "name": a["name"],
            "year": a["year"],
            "path": a["filename"],
        }


    # Dump result in unique JSON file
    sorted_corpus = sorted(corpus, key=lambda x: x["metadata"]["year"])
    json_file = open(os.path.join(pieceName, "corpus.json"), "w")
    json.dump(sorted_corpus, json_file, indent=2)

def histograms_generation():
    os.makedirs(os.path.join(pieceName,"plots"), exist_ok=True)
    corpus = import_json_file(os.path.join(pieceName,"corpus.json"))
    colors = []
    for edition in corpus: # set color randomly
        colors.append((np.random.random(), np.random.random(), np.random.random()))
    for key in corpus[0]["statistics"].keys(): # generate plot for each parameter
        objects = []
        values = []
        for edition in corpus:
            objects.append(edition["metadata"]["name"].capitalize())
            values.append(edition["statistics"][key])

        colorByGroupHistogram(objects, values, key, colors, pieceName+"/plots")




# FUNCTIONS calling

musicxml_analysis()

histograms_generation()
