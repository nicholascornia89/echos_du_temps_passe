""" 
This scripts will extract all stream elements of a Music21 score and
organize them as a csv file (or JSON) for further analysis

I am not concerned to voicing and layout, thus I a m flattening all voices into one

"""

import os
import music21 as m21
import csv, json, xml

# Import MusicXML paths
transcriptionsPath = "../../../encoded_music/project_transcriptions/"
sonataPath = os.path.join(transcriptionsPath, "bach_wtc/BWV853/musicxml/")
pieceName = "BWV853"
urtextName = pieceName + "_durr"
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


def m21stream2dict(score, id_name):
    # assign static ids to
    id_counter = 1
    id_base = id_name
    score_dict = []
    score_statistics = {
        "measures": 0,
        "notes": len(score.flatten().getElementsByClass("GeneralNote")),
        "slurs": len(score.flatten().getElementsByClass("Slur")),
        "slurs_average_density": 0,
        "dynamics": len(
            score.flatten().getElementsByClass(
                ("Dynamic", "Crescendo", "Decrescendo", "Diminuendo")
            )
        ),
        "expressions": len(score.flatten().getElementsByClass("TextExpression")),
        "tempos": len(
            score.flatten().getElementsByClass(("TempoIndication", "MetronomeMark"))
        ),
        "articulations": 0,
        # "pedals": {"counter": 0, "density": 0},
    }
    # get general notes
    art_count = 0
    for el in score.flatten().getElementsByClass("GeneralNote"):
        el.id = id_base + str(id_counter)
        id_counter += 1
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": "note",
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
                "type": "GeneralNote",
            }
        )
        if len(el.articulations) > 0:
            for articulation in el.articulations:
                # get Articulation
                art_count += 1
                articulation.id = id_base + str(id_counter)
                id_counter += 1
                score_dict.append(
                    {
                        "measure_start": el.measureNumber,
                        "measure_end": "",
                        "object": articulation,
                        "value": articulation.name,
                        "id": articulation.id,
                        "quarterlength": articulation.quarterLength,
                        "offset": articulation.offset,
                        "type": "Articulation",
                    }
                )
    score_statistics["articulations"] = art_count
    # get slurs
    slurLenghtSum = 0
    for el in score.flatten().getElementsByClass("Slur"):
        # length of slur = offset distance between extreme notes
        el.id = id_base + str(id_counter)
        id_counter += 1
        spanner_length = (
            el.getSpannedElements()[-1].offset - el.getSpannedElements()[0].offset
        )
        slurLenghtSum += spanner_length
        score_dict.append(
            {
                "measure_start": el.getSpannedElements()[0].measureNumber,
                "measure_end": el.getSpannedElements()[-1].measureNumber,
                "object": el,
                "value": "slur",
                "id": el.id,
                "quarterlength": spanner_length,
                "offset": el.offset,
                "type": "Slur",
            }
        )
    # get dynamics
    for el in score.flatten().getElementsByClass("Dynamic"):
        el.id = id_base + str(id_counter)
        id_counter += 1
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": el.value,
                "id": el.id,
                "quarterlength": "",
                "offset": "",
                "type": "DynamicPoint",
            }
        )

    # get cresc. decrc. and diminuendo
    for el in score.flatten().getElementsByClass(
        ("Crescendo", "Decrescendo", "Diminuendo")
    ):
        try:
            el.id = id_base + str(id_counter)
            id_counter += 1
            score_dict.append(
                {
                    "measure_start": el.getSpannedElements()[0].measureNumber,
                    "measure_end": el.getSpannedElements()[-1].measureNumber,
                    "object": el,
                    "value": el.value,
                    "id": el.id,
                    "quarterlength": "",
                    "offset": "",
                    "type": "DynamicRegion",
                }
            )
        except AttributeError:  # Diminuendo case
            el.id = id_base + str(id_counter)
            id_counter += 1
            score_dict.append(
                {
                    "measure_start": el.getSpannedElements()[0].measureNumber,
                    "measure_end": el.getSpannedElements()[-1].measureNumber,
                    "object": el,
                    "value": "diminuendo",
                    "id": el.id,
                    "quarterlength": "",
                    "offset": "",
                    "type": "DynamicRegion",
                }
            )
    # get TextExpressions (rall. other instructions)
    for el in score.flatten().getElementsByClass("TextExpression"):
        el.id = id_base + str(id_counter)
        id_counter += 1
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": el.content,
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
                "type": "TextExpression",
            }
        )
    # get Tempo and Metronome Marks
    for el in score.flatten().getElementsByClass("TempoIndication"):
        el.id = id_base + str(id_counter)
        id_counter += 1
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": str(el.text),
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
                "type": "TempoIndication",
            }
        )

    for el in score.flatten().getElementsByClass("MetronomeMark"):
        el.id = id_base + str(id_counter)
        id_counter += 1
        score_dict.append(
            {
                "measure_start": el.measureNumber,
                "measure_end": "",
                "object": el,
                "value": str(el.text) + " " + str(el.number),
                "id": el.id,
                "quarterlength": el.quarterLength,
                "offset": el.offset,
                "type": "MetronomeMark",
            }
        )

    # get Pedal: not supported by Music21...

    # compute number of measures
    max_measure = 0
    for item in score_dict:
        if int(item["measure_start"]) > max_measure:
            max_measure = int(item["measure_start"])
        else:
            pass
    score_statistics["measures"] = max_measure
    # calculate density based on measure length
    time_signature = (
        score.parts[0].getElementsByClass("Measure")[0].timeSignature.ratioString
    )

    time_signature = time_signature.split("/")
    measureQuarterLength = float(time_signature[0]) * 4 / float(time_signature[1])
    a = float(slurLenghtSum)
    b = float(score_statistics["slurs"]) * measureQuarterLength
    score_statistics["slurs_average_density"] = a / b

    return score_dict, score_statistics, score


def csv2dict(csv_filename):
    f = open(csv_filename, "r")
    reader = csv.DictReader(f)
    d = {"items": []}
    for row in reader:
        d["items"].append(row)
    return d


def diff_streams(u, a):
    # stores the differences in a list of Music21 IDs
    # simple version, assuming len(a) > len(u)
    diff_list = []
    n = len(u)
    m = len(a)
    stay = True
    i = j = 0
    while stay:
        if u[i]["object"] == a[j]["object"]:  # if streams are equal skip
            i += 1
            j += 1
        else:  # if streams are different, append id to be colored
            diff_list.append(
                {
                    "id": a[j]["id"],
                    "object": a[j]["object"],
                    "measure": a[j]["measure_start"],
                    "type": a[j]["type"],
                }
            )
            j += 1

        if j >= m:
            break
        if i >= n:
            break
    return diff_list


def m21color_objects(stream, id_list, color="red"):
    # colors objects in a stream given a list of ids
    for i in id_list:
        # exclude notes
        if i["type"] == "GeneralNote":
            pass
        else:
            if stream.flatten().getElementById(i["id"]) != None:
                stream.flatten().getElementById(i["id"]).style.color = color
            else:  # articulation case
                for note in stream.flatten().getElementsByClass("GeneralNote"):
                    for articulation in note.articulations:
                        if articulation.id == i["id"]:
                            articulation.style.color = color

    return stream


# Urtext analysis
urtextDictionary, urtextStatistics, urtextScore = m21stream2dict(urtextScore, "urtext")
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
