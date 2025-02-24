""" 
This scripts will extract all stream elements of a Music21 score and
organize them as a csv file (or JSON) for further analysis

I am not concerned to voicing and layout, thus I a m flattening all voices into one

"""

import os
import music21 as m21
import csv, json

# Import MusicXML paths
transcriptionsPath = "../../../encoded_music/project_transcriptions/"
sonataPath = os.path.join(transcriptionsPath, "scarlatti_sonatas/K9/musicxml/")
pieceName = "K9"
urtextName = pieceName + "_gilbert"
arrangements = [
    {"name": "tausig"},
    {"name": "buonamici"},
    {"name": "dunhill"},
    {"name": "czerny"},
]


# Import Urtext as Music21 object
# urtextFilename = sonataPath + urtextName + ".musicxml"
# urtextFilename = "K9_gilbert.musicxml"
# urtextScore = m21.converter.parse(urtextFilename)
# arrangementFilename = "K9_czerny.musicxml"
# arrangementScore = m21.converter.parse(arrangementFilename)

# Import Urtext as Music21 object
urtextFilename = os.path.join(sonataPath, urtextName + ".musicxml")
urtextScore = m21.converter.parse(urtextFilename)
arrangementsFilename = []
arrangementsScore = []
for a in arrangements:
    a["filename"] = os.path.join(sonataPath, pieceName + "_" + a["name"] + ".musicxml")
    a["score"] = m21.converter.parse(a["filename"])


def dict2csv(dict_list, out_filename):
    f = open(out_filename, "w")
    # assumed dict list structure as uniform
    # json = [ {key1: ... , key2: ... }, {key1: ... , key2: ... }]
    field_names = list(dict_list[0].keys())
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(dict_list)
    f.close()


def m21stream2dict(score):
    score_dict = []
    # get general notes
    for el in score.flatten().getElementsByClass("GeneralNote"):
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": "note",
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
            }
        )
    # get slurs
    for el in score.flatten().getElementsByClass("Slur"):
        # length of slur = offset distance between extreme notes
        spanner_length = (
            el.getSpannedElements()[-1].offset - el.getSpannedElements()[0].offset
        )
        score_dict.append(
            {
                "measure_start": el.getSpannedElements()[0].measureNumber,
                "measure_end": el.getSpannedElements()[-1].measureNumber,
                "object": el,
                "value": "slur",
                "id": el.id,
                "quarterlength": spanner_length,
                "offset": el.offset,
            }
        )

    # get dynamics
    print(
        "Number of dynamic elements:",
        len(
            score.flatten().getElementsByClass(
                ("Dynamic", "Crescendo", "Decrescendo", "Diminuendo")
            )
        ),
    )
    for el in score.flatten().getElementsByClass("Dynamic"):
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": el.value,
                "id": el.id,
                "quarterlength": "",
                "offset": "",
            }
        )

    # get cresc. decrc. and diminuendo

    for el in score.flatten().getElementsByClass(
        ("Crescendo", "Decrescendo", "Diminuendo")
    ):
        try:
            score_dict.append(
                {
                    "measure_start": el.getSpannedElements()[0].measureNumber,
                    "measure_end": el.getSpannedElements()[-1].measureNumber,
                    "object": el,
                    "value": el.value,
                    "id": el.id,
                    "quarterlength": "",
                    "offset": "",
                }
            )
        except AttributeError:  # Diminuendo case
            score_dict.append(
                {
                    "measure_start": el.getSpannedElements()[0].measureNumber,
                    "measure_end": el.getSpannedElements()[-1].measureNumber,
                    "object": el,
                    "value": "diminuendo",
                    "id": el.id,
                    "quarterlength": "",
                    "offset": "",
                }
            )

    print(
        "Number of expression elements:",
        len(score.flatten().getElementsByClass("TextExpression")),
    )
    # get TextExpressions (rall. other instructions)
    for el in score.flatten().getElementsByClass("TextExpression"):
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": el.content,
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
            }
        )

    # get Pedal

    # get Articulation
    print(
        "Number of articulation elements:",
        len(score.flatten().getElementsByClass("Articulation")),
    )
    # get TextExpressions (rall. other instructions)
    for el in score.flatten().getElementsByClass("Articulation"):
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": el.name,
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
            }
        )

    return score_dict


# Urtext analysis
urtextDictionary = sorted(m21stream2dict(urtextScore), key=lambda x: x["measure_start"])

try:
    os.makedirs(pieceName)
except FileExistsError:
    pass
dict2csv(urtextDictionary, os.path.join(pieceName, "urtext.csv"))


# Arrangements analysis
for a in arrangements:
    print("Current arrangement: ", a["name"])
    arrangementDictionary = m21stream2dict(a["score"])
    for el in arrangementDictionary:
        if isinstance(el["measure_start"], int):
            pass
        else:
            print(el)

    arrangementDictionary = sorted(
        arrangementDictionary, key=lambda x: x["measure_start"]
    )
    dict2csv(arrangementDictionary, os.path.join(pieceName, a["name"] + ".csv"))
