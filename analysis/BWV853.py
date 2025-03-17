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
urtextName = pieceName + "_durr"
arrangements = [
    {"name": "czerny"},  # 1830
    {"name": "bischoff"},  # 1889
    {"name": "busoni"},  # 1894
    {"name": "wouters"},  # 1899
    {"name": "bartok"},  # 1907
    {"name": "morgan"},  # 1912
    {"name": "dejong"},  # 1925
    {"name": "sporck"},  # 1914
    {"name": "selva"},  # 1915
]


# Import Urtext as Music21 object
urtextFilename = os.path.join(piecePath, urtextName + ".musicxml")
urtextScore = m21.converter.parse(urtextFilename)
for a in arrangements:
    a["filename"] = os.path.join(piecePath, pieceName + "_" + a["name"] + ".musicxml")
    a["score"] = m21.converter.parse(a["filename"])


# Urtext analysis


def musicxml_analysis(urtextScore):
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
        """ check if every object has a measure number
        for el in arrangementDictionary:
            if isinstance(el["measure_start"], int):
                pass
            else:
                print(el) """

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
    for file in os.listdir(pieceName):
        # check extension
        if os.path.splitext(file)[1] == ".json":
            # load json file as dictionary
            json_name = os.path.splitext(file)[0].split("_")[0]
            query = list(
                filter(lambda x: x[1]["name"] == json_name, enumerate(arrangements))
            )
            if len(query) > 0:
                arrangements[query[0][0]]["plot_name"] = file.split("_")[0].capitalize()
                arrangements[query[0][0]]["statistics"] = import_json_file(
                    os.path.join(pieceName, file)
                )

    # set colors
    colors = []
    for arrangement in arrangements:
        colors.append((np.random.random(), np.random.random(), np.random.random()))

    for key in arrangements[0]["statistics"].keys():
        objects = []
        values = []
        for arrangement in arrangements:
            objects.append(arrangement["plot_name"])
            values.append(arrangement["statistics"][key])

        colorByGroupHistogram(objects, values, key, colors, pieceName)


# CODE

# musicxml_analysis(urtextScore)
histogram_generations()
