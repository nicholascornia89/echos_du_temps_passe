import matplotlib.pyplot as plt
import numpy as np
import csv, json, xml
import os
import music21 as m21


# FUNCTIONS
def import_json_file(fn):
    # Import json file
    with open(fn, "r") as f:
        json_file = json.load(f)
        # print(json_file)
        return json_file


def dict2csv(dict_list, out_filename):
    f = open(out_filename, "w")
    # assumed dict list structure as uniform
    # json = [ {key1: ... , key2: ... }, {key1: ... , key2: ... }]
    field_names = list(dict_list[0].keys())
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(dict_list)
    f.close()


def csv2dict(csv_filename):
    f = open(csv_filename, "r")
    reader = csv.DictReader(f)
    d = {"items": []}
    for row in reader:
        d["items"].append(row)
    return d


def colorByGroupHistogram(objects, values, value_label, colors, base_path):
    fig, ax = plt.subplots()
    # figure size in inches
    plt.rcParams["figure.figsize"] = (14, 6)
    # best location for legend
    # plt.rcParams["legend.loc"] = "best"
    bar_labels = objects
    bar_colors = colors
    ax.bar(objects, values, label=bar_labels, color=bar_colors)
    ax.set_ylabel("value")
    ax.set_title(value_label.capitalize().replace("_", " ") + " analysis")
    # ax.legend(title=value_label)
    plt.tight_layout()
    plt.rcParams.update({"figure.autolayout": True})
    plt.style.use("fast")
    plt.savefig(os.path.join(base_path, "statistics_" + value_label + ".png"), dpi=600)


def totalAnnotationsPlot(names, values):
    fig, ax = plt.subplots()
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["legend.loc"] = "best"
    ax.set_title("Total annotations")
    plt.tight_layout()
    plt.rcParams.update({"figure.autolayout": True})
    plt.style.use("fast")
    plt.plot(names, values)
    plt.savefig(os.path.join(base_path, "statistics_total" + ".png"), dpi=600)


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


def m21stream2dict(score, id_name):
    # assign static ids to
    id_counter = 1
    id_base = id_name
    score_dict = []
    total_annotations = 0
    score_statistics = {
        "measures": 0,
        "notes": len(score.flatten().getElementsByClass("GeneralNote")),
        "total_annotations": 0,
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
        "fingerings": 0
        # "pedals": {"counter": 0, "density": 0},
    }

    # get general notes
    art_count = 0
    fingering_count = 0
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
                # get fingerings
                if articulation.name == "fingering":
                    fingering_count += 1
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
                            "type": "Fingering",
                        }
                    )
                else:
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
    score_statistics["fingerings"] = fingering_count

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

            if el.getSpannedElements()[0].measureNumber == None:
                score_dict[-1]["measure_start"] = score_dict[-1]["measure_end"]
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

    # summing up all annotations
    for key in score_statistics.keys():
        # print(f"Current key: {key}")
        if (
            key == "measures"
            or key == "notes"
            or key == "slurs_average_density"
            or key == "total_annotations"
        ):
            pass
        else:
            # print("adding to total annotations")
            score_statistics["total_annotations"] += score_statistics[key]

    # compute number of measures
    max_measure = 0

    """ check if every object has a measure number
    for el in score_dict:
        if isinstance(el["measure_start"], int):
            pass
        else:
            print(el)
    """

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
