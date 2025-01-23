'''
This script analyses imported metadata from the FAAM platform in CSV format

'''

import csv
import json
#import numpy
#import mathplotlib

def csv2dict(csv_filename): # dumps a CSV into dictionary with main property "items"
	f = open(csv_filename,'r')
	reader = csv.DictReader(f)
	d = {"items": []}
	for row in reader:
		d["items"].append(row)
	return d

def dict2json(dictionary,json_filename): 	#dumps a dictionary into a JSON file
	json_file = open(json_filename,'w')
	json.dump(dictionary,json_file,indent=2,ensure_ascii=False )
	return print("Export completed.")

def inputCsv2faamJson(manifestations_dict,works_dict,annotations_dict): 	# Cleans-up, organizes and collates duplicates
	# Initialize main FAAM categories
	FAAM = {
	"manifestations": [],
	"agents": [],
	"musicalWorks": [],
	"annotations": []
	 }
	#manifestation structure, the other follows
	'''
	manifestation structure
	{
		"FAAM-ID": 
		"title":
		"permalink":
		"musicalWorks": [{"workName"}]
		"agents": [{"agentName": ,"agentRole":}]
		"annotations": [{"annotationName": }]
		
	}
	'''
	# Generate manifestations
	for row in manifestations_dict["items"]:
		#check if FAAM-ID changed
		try:
			current_manifestation = FAAM["manifestations"][-1]
			if row["\ufeffFAAM-ID"] == current_manifestation["FAAM-ID"]: # do not create new manifestation keep adding metadata
				if any(x.get("workName") == row["Musical Works"] for x in current_manifestation["musicalWorks"]):
					pass
				else:
					current_manifestation["musicalWorks"].append({"workName": row["Musical Works"]})
				if any(x.get("agentName") == row["[Agent] Agent"] for x in current_manifestation["agents"]):
					pass
				else:
					current_manifestation["agents"].append(
															{"agentName": row["[Agent] Agent"],
															 "agentRole": row["[Agent] Role"]}	
																)
				if any(x.get("annotationName") == row["Editorial annotations"] for x in current_manifestation["annotations"]  ):
					pass
				else:
					current_manifestation["annotations"].append({"annotationName": row["Editorial annotations"]}) # current manifestation case
			else: # new manifestation case
				FAAM["manifestations"].append({
				"FAAM-ID": row["\ufeffFAAM-ID"],
				"title": row["Title"],
				"permalink": row["Permalink"],
				"musicalWorks": [{"workName": row["Musical Works"]}],
				"agents": [{"agentName": row["[Agent] Agent"], "agentRole": row["[Agent] Role"]}],
				"annotations": [{"annotationName": row["Editorial annotations"]}]

				})
		except IndexError: # first element case
			FAAM["manifestations"].append({
				"FAAM-ID": row["\ufeffFAAM-ID"],
				"title": row["Title"],
				"permalink": row["Permalink"],
				"musicalWorks": [{"workName": row["Musical Works"]}],
				"agents": [{"agentName": row["[Agent] Agent"], "agentRole": row["[Agent] Role"]}],
				"annotations": [{"annotationName": row["Editorial annotations"]}]

				})


	# Generate works
	for row in musicalWorks["items"]:
		try:

		# TO BE CONTINUED
		except IndexError: # first element
			FAAM["musicalWorks"].append(
				{
					"workName": row["\ufeffName"],
					"qid": row["Wikidata QID"],
					"composers": [row["composer"]],
					"arrangers": [row["arrangers"]],
					"annotations": [row["Editorial annotations"]],
					"FAAM-IDs": [],
					"occurrence": 0
				}

				)
	# Generate annotations
	# TO BE CONTINUED



	return FAAM

def faaamStatistics(FAAM): #Generates statistics for FAAM JSON
	# Unique agents, musicalWorks and annotations
	for manifestation in FAAM["manifestations"]:
		for musicalWork in manifestation["musicalWorks"]: #add manif. to musical works
			if musicalWork["workName"] == "":
				print(manifestation)
				input()
			# check if the work's Name is already present
			query = list(filter(lambda x: x[1].get('workName') == musicalWork["workName"], enumerate(FAAM["musicalWorks"])))
			if len(query) >0:
				# update occurrence
				FAAM["musicalWorks"][query[0][0]]["occurrence"] +=1
				FAAM["musicalWorks"][query[0][0]]["FAAM-IDs"].append(manifestation["FAAM-ID"])
			else: #append new element, normally not necessary!
				
				FAAM["musicalWorks"].append(
					{
					"workName": musicalWork["workName"],
					"qid": "",
					"composers": [],
					"arrangers": [],
					"annotations": [],
					"FAAM-IDs": [manifestation["FAAM-ID"]],
					"occurrence": 1
					})

		for agent in manifestation["agents"]: #add agent to agents list
			#to be continued...
		for annotation in manifestation["annotations"]: # add annotations to annotations list
	return FAAM



# CODE
#print("Insert the input CSV filename (with extension): \n")
#input_csv_filename = input()
#TEST
date = "20250123"

input_manifestations_csv_filename = "FAAM-scarlatti_export_20250122.csv"
input_works_csv_filename = "FAAM-scarlatti-works_export-"+date+".csv"
input_annotations_csv_filename = "../FAAM_annotations/FAAM-annotations_export-"+date+".csv"
output_json_filename = input_csv_filename[:-4]+".json"

print("Loading CSVs into Python dictionary...")
manifestations_dict = csv2dict(input_manifestation_filename)
works_dict = csv2dict(input_works_csv_filename)
annotations_dict = csv2dict(input_annotations_csv_filename)

print("Clean-up and export to JSON...")
FAAM = inputCsv2faamJson(manifestations_dict,works_dict,annotations_dict)
FAAM = faaamStatistics(FAAM)
dict2json(FAAM,output_json_filename)
