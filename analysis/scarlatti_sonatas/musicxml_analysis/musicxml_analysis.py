'''
This script will extract information about specific objects in a MusicXML file
'''

import sys
import os
import json
import music21 as m21

def musicxml2list(xml):
	m21score = m21.converter.parse(xml)
	listscore = []
	for part in m21score.parts:
		instrument = part.getInstrument().instrumentName

		for note in part.flat.notes:
			if note.isChord:
				chord_notes = []
				for chord_note in note.pitches:
					chord_notes.append(chord_note.name)
				listscore.append([instrument,chord_notes,note.quarterLength,note.volume.realized])
			else:	
				listscore.append([instrument,note.pitch.name,note.quarterLength,note.volume.realized])

	print(listscore[:10])

def slurAnalysis(s):
	results = {
	"slur": {
		"count": 0,
		"density": 0
		}
	}
	element_counter = 0
	density_counter = 0
	for el in s.flatten().getElementsByClass(m21.spanner.Slur):
		element_counter+=1
		density_counter+=len(el.getSpannedElements())
	
	results["slur"]["count"] = element_counter
	try:
		results["slur"]["density"] = density_counter/element_counter
	except ZeroDivisionError:
		results["slur"]["density"] = 0

	return results

def textExpressionAnalysis(s):
	results = {
	"text": {
		"count": 0
	}
	}
	element_counter = 0
	#density_counter = 0
	for el in s.flatten().getElementsByClass(m21.expressions.TextExpression):
		element_counter+=1
		#density_counter+=len(el)
	results["text"]["count"] = element_counter
	return results

def dynamicsAnalysis(s):
	results = {
	"dynamics": {
		"count": 0
		},
	"hairpin": {
		"count": 0,
		"density": 0
		}
	}
	element_counter = 0
	#add static dynamics
	for el in s.flatten().getElementsByClass(m21.dynamics.Dynamic):
		element_counter+=1
	results["dynamics"]["count"] = element_counter
	element_counter = 0
	density_counter = 0
	#hairpin crescendo
	for el in s.flatten().getElementsByClass(m21.dynamics.Crescendo):
		element_counter+=1
		density_counter+=len(el.getSpannedElements())
	#hairpin decrescendo
	for el in s.flatten().getElementsByClass(m21.dynamics.Crescendo):
		element_counter+=1
		density_counter+=len(el.getSpannedElements())

	results["hairpin"]["count"] = element_counter
	try:
		results["hairpin"]["density"] = density_counter/element_counter
	except ZeroDivisionError:
		results["hairpin"]["density"] = 0

	return results

def getElementsInScore(s):
	for el in s.flatten():
		print(el)
		input()

# Import MusicXML paths
transcriptionsPath = "../../../encoded_music/project_transcriptions/"
sonataPath = transcriptionsPath+"scarlatti_sonatas/K9/musicxml/"
pieceName = "K9"
urtextName = pieceName+"_gilbert"
arrangements = ["tausig","buonamici","dunhill","czerny"]

# Generate result dictionary
results = {}
results_json_filename = "musicxml_analysis.json"

# Import Urtext as Music21 object
urtextFilename = sonataPath+urtextName+".musicxml"
arrangementsFilename = []
for a in arrangements:
	arrangementsFilename.append(sonataPath+pieceName+"_"+a+".musicxml")
urtextScore = m21.converter.parse(urtextFilename)
arrangementsScore = []
for a in arrangementsFilename:
	arrangementsScore.append(m21.converter.parse(a))

#print("Urtext results:")
results["Urtext_"+urtextName] = {
		"slur": slurAnalysis(urtextScore),
		"text": textExpressionAnalysis(urtextScore),
		"dynamics": dynamicsAnalysis(urtextScore)
	}

for i in range(len(arrangementsScore)):
	#print(arrangements[i].upper()+" results:")
	results[arrangements[i]] = {
		"slur": slurAnalysis(arrangementsScore[i]),
		"text": textExpressionAnalysis(arrangementsScore[i]),
		"dynamics": dynamicsAnalysis(arrangementsScore[i])
	}
	
	
# Save results
results_json_file = open(results_json_filename,'w')
json.dump(results,results_json_file,indent=2)






