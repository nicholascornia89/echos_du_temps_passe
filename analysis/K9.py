"""
Unfied K9 script
"""
import sys

sys.path.append(".")  # import utilities functions from model directory.

import os
import csv, json
import music21 as m21
from model import *


# Import MusicXML paths
transcriptionsPath = "../encoded_music/project_transcriptions/"
pieceName = "K9"
piecePath = os.path.join(transcriptionsPath, pieceName, "musicxml")

arrangements = [
    {"name": "gilbert", "year": 1984, "type": "urtext"},
    {"name": "czerny", "year": 1830, "type": "arrangement"},
    {"name": "tausig", "year": 1865,"type": "arrangement"},
    {"name": "wouters", "year": 1890,"type": "arrangement"},
    {"name": "buonamici", "year": 1902, "type": "arrangement"},
    {"name": "oesterle", "year": 1904,"type": "arrangement"},
    {"name": "esposito", "year": 1905,"type": "arrangement"},
    {"name": "longo", "year": 1906,"type": "arrangement"},
    {"name": "dunhill", "year": 1917,"type": "arrangement"},
    {"name": "sauer", "year": 1942,"type": "arrangement"},
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

