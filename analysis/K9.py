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
sonataPath = os.path.join(transcriptionsPath, "scarlatti_sonatas/K9/musicxml/")
pieceName = "K9"
urtextName = pieceName + "_gilbert"
arrangements = [
    {"name": "buonamici"},
    {"name": "czerny"},
    {"name": "dunhill"},
    {"name": "esposito"},
    {"name": "longo"},
    {"name": "oesterle"},
    {"name": "sauer"},
    {"name": "tausig"},
    {"name": "wouters"},
]


# Import Urtext as Music21 object
urtextFilename = os.path.join(sonataPath, urtextName + ".musicxml")
urtextScore = m21.converter.parse(urtextFilename)
arrangementsFilename = []
arrangementsScore = []
for a in arrangements:
    a["filename"] = os.path.join(sonataPath, pieceName + "_" + a["name"] + ".musicxml")
    a["score"] = m21.converter.parse(a["filename"])


def musicxml_analysis(urtextScore):
    # Urtext analysis
    urtextDictionary, urtextStatistics, urtextScore = m21stream2dict(
        urtextScore, "urtext"
    )
    urtextDictionary = sorted(urtextDictionary, key=lambda x: x["measure_start"])

    # Create subdirectories
    os.makedirs(pieceName, exist_ok=True)
    os.makedirs("./" + pieceName + "/diff", exist_ok=True)

    dict2csv(urtextDictionary, os.path.join(pieceName, "urtext.csv"))
    json_file = open(os.path.join(pieceName, "urtext_statistics.json"), "w")
    json.dump(urtextStatistics, json_file, indent=2)

    # Arrangements analysis
    for a in arrangements:
        print("Current arrangement: ", a["name"])
        arrangementDictionary, arrangementStatistics, a["score"] = m21stream2dict(
            a["score"], a["name"]
        )

        arrangementDictionary = sorted(
            arrangementDictionary, key=lambda x: x["measure_start"]
        )

        dict2csv(arrangementDictionary, os.path.join(pieceName, a["name"] + ".csv"))
        json_file = open(os.path.join(pieceName, a["name"] + "_statistics.json"), "w")
        json.dump(arrangementStatistics, json_file, indent=2)

        # generate difference list
        diff = diff_streams(urtextDictionary, arrangementDictionary)
        diff_score = m21color_objects(a["score"], diff)

        # the export to MusicXML is not working properly. Slurs are not colored.
        diff_filename = "./" + pieceName + "/diff/" + a["name"] + "_diff.musicxml"
        # diff_score.write(".musicxml", diff_filename)
        xml_converter = m21.converter.subConverters.ConverterMusicXML()
        xml_converter.write(
            obj=diff_score,
            fmt="musicxml",
            makeNotation=True,
            compress=False,
            fp=diff_filename,
        )

        # export to CSV
        diff_filename = "./" + pieceName + "/diff/" + a["name"] + "_diff.csv"
        dict2csv(diff, diff_filename)


# Histogram generation


def histogram_generations():
    arrangements = []
    for file in os.listdir(pieceName):
        # check extension
        if os.path.splitext(file)[1] == ".json":
            # load json file as dictionary
            arrangements.append(
                {
                    "name": file.split("_")[0].capitalize(),
                    "statistics": import_json_file(os.path.join(pieceName, file)),
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

        colorByGroupHistogram(objects, values, key, colors, pieceName)


# CODE

musicxml_analysis(urtextScore)

histogram_generations()
