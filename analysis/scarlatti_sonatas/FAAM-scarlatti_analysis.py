'''
This script analyses imported metadata from the FAAM platform in CSV format

'''

import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network
import networkx as nx

def xy_horizontalhistogram(x_list,y_list,xValue,title): #inputs 2 lists and returns histogram
	fig, ax = plt.subplots()
	# data
	y_pos = np.arange(len(y_list))
	x_pos = np.arange(len(x_list))
	ax.barh(y_list,x_list, color= "#d63a19", height = 0.7)
	ax.set_yticklabels(y_list,fontsize=10)
	ax.set_xticks(np.arange(12))
	ax.tick_params(axis='both', which='major', pad=1)
	ax.set(xlim=[0, 12], xlabel=xValue, ylabel="",
       title=title)
	plt.tight_layout()
	plt.rcParams.update({'figure.autolayout': True})
	plt.style.use('fast')
	plt.savefig('histogram.png',dpi=600)

def csv2dict(csv_filename): # dumps a CSV into dictionary with main property "items"
	f = open(csv_filename,'r')
	reader = csv.DictReader(f)
	d = {"items": []}
	for row in reader:
		d["items"].append(row)
	return d

def json2dict(fn):
	#Import json file
	with open(fn, 'r') as f:
		dictionary = json.load(f)
		return dictionary

def add_node(net,node_id,label,color,value,title):
	return net.add_node(
		node_id,
		label = label,
		color= color,
		value= value,
		title= title
	)	

def generate_network(FAAM): # returns a Networkx graph given the FAAM elements dictionary
	net = nx.Graph()
	# node attributes
	nodes_colors = {
	"manifestation": "#d63a19",
	"annotation": "#017cb1",
	"work": "#8b9a66",
	"agent": "#d49d33"}

	# base urls
	faamUrlManifestation = "https://faam.laboxix-xx.be/viewer.p/1/2925/object/11132-"
	wikidataUrl = "https://wikidata.org/entity/"

	#NODES
	# add manifestation nodes
	for manifestation in FAAM["manifestations"]:
		url ="<a href=\'"+manifestation["FAAMUrl"]+">"+manifestation["title"]+", "+manifestation["FAAM-ID"]+"</a>"
		title ="<body>"+url+"</body>"
		add_node(net,manifestation["FAAM-ID"],manifestation["title"],nodes_colors["manifestation"],10*len(manifestation["musicalWorks"]),title)
	# add work nodes
	for work in FAAM["musicalWorks"]:
		if "qid" in work: # exclude works without qid
			url = "<a href=\'"+work["wikidataUrl"]+">"+work["workName"]+", "+work["qid"]+"</a>"
			title ="<body>"+url+"</body>"
			add_node(net,work["qid"],work["workName"],nodes_colors["work"],10**work["occurrence"],title)
	# add annotation nodes
	for anno in FAAM["annotations"]:
		url = "<a href=\'"+wikidataUrl+anno["qid"]+">"+anno["annotationName"]+", "+anno["qid"]+"</a>"
		
		add_node(net,anno["qid"],anno["annotationName"],nodes_colors["annotation"],5,title)
	# add agent nodes
	for agent in FAAM["agents"]:
		if "qid" in agent: # exclude publishers for now
			url = "<a href=\'"+wikidataUrl+agent["qid"]+">"+agent["agentName"]+", "+agent["qid"]+"</a>"
			title ="<body>"+url+"</body>"
			add_node(net,agent["qid"],agent["agentName"],nodes_colors["agent"],10000,title)

	#EDGES
	for work in FAAM["musicalWorks"]:
		#for composer in work["composers"]:
			#net.add_edge(work["qid"],composer["qid"],weight=1)
		for arranger in work["arrangers"]:
			if arranger["qid"] == "":
				pass
			else:
				net.add_edge(work["qid"],arranger["qid"],weight=10)
		for annotation in work["annotations"]:
			if annotation["qid"] == "":
				pass
			else:
				net.add_edge(work["qid"],annotation["qid"],weight=1) 

	return net

def pyvis_visualization(net,net_filename):
	layout = nx.spring_layout(net)
	visualization=Network(height="1200px", width="1200px", bgcolor="#1C1A19", font_color="#f8f7f4", directed=False,select_menu=True,filter_menu=False,notebook=False)
	
	# The visualisation can be changed using the native vis Physics settings in options.
	# https://visjs.github.io/vis-network/docs/network/physics.html
	'''for i in visualization.nodes:
		#node_id = i["id"]
		#if node_id in layout:
			#i["x"], i["y"] = layout[node_id][0]*1000, layout[node_id][1]*1000
	visualization.force_atlas_2based(gravity=-5000,
							spring_strength=0.5,
							central_gravity=0,
							spring_length=10,
							damping=0.4,overlap=1)
	'''
	visualization.from_nx(net)
	visualization.toggle_physics(False)
	visualization.show_buttons(filter_=['nodes','physics'])
	
	options = """
			var options = {
   					"configure": {
						"enabled": false
   							},
  					"edges": {
					"color": {
	  				"inherit": true
						},
					"smooth": false
  					},
  					"physics": {
						"forceAtlas2Based": {
	  					"gravitationalConstant": -20,
	  					"springLength": 1,
	  					"springConstant": 1.0,
	  					"avoidOverlap": 0,
	  					"damping":0

							},
						"maxVelocity": 1,
						"minVelocity": 0.25
  						}
					}
				"""
	visualization.set_options(options)
	#visualization.show(net_filename+'.html',notebook=False)
	#input()
	#visualization.write_html(name='example.html',notebook=False,open_browser=False)
	visualization.save_graph(net_filename+'.html')
	
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
	# base urls
	faamUrlManifestation = "https://faam.laboxix-xx.be/viewer.p/1/2925/object/11132-"
	wikidataUrl = "https://wikidata.org/entity/"
	# Generate manifestations
	for row in manifestations_dict["items"]:
		#check if FAAM-ID changed
		try:
			current_manifestation = FAAM["manifestations"][-1]
			if row["FAAM-ID"] == current_manifestation["FAAM-ID"]: # do not create new manifestation keep adding metadata
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
				"FAAM-ID": row["FAAM-ID"],
				"FAAMUrl": faamUrlManifestation+row['\ufeff"Object ID"'],
				"title": row["Title"],
				"permalink": row["Permalink"],
				"musicalWorks": [{"workName": row["Musical Works"]}],
				"agents": [{"agentName": row["[Agent] Agent"], "agentRole": row["[Agent] Role"]}],
				"annotations": [{"annotationName": row["Editorial annotations"]}]

				})
		except IndexError: # first element case
			FAAM["manifestations"].append({
				"FAAM-ID": row["FAAM-ID"],
				"FAAMUrl": faamUrlManifestation+row['\ufeff"Object ID"'],
				"title": row["Title"],
				"permalink": row["Permalink"],
				"musicalWorks": [{"workName": row["Musical Works"]}],
				"agents": [{"agentName": row["[Agent] Agent"], "agentRole": row["[Agent] Role"]}],
				"annotations": [{"annotationName": row["Editorial annotations"]}]

				})
	# Generate works
	for row in works_dict["items"]:
		try:
			query = list(filter(lambda x: x[1].get('workName') == row["\ufeffName"], enumerate(FAAM["musicalWorks"]) ))
			current_work = FAAM["musicalWorks"][query[0][0]]
			# add arrangers
			if any(x.get("agentName") == row["arranger"] for x in current_work["arrangers"]):
				pass
			else:
				# append new arranger
				current_work["arrangers"].append(
					{
						"agentName": row["arranger"],
						"qid": row["arranger QID"]					
					}

					)
				current_work["occurrence"]+=1	

		except IndexError: # first element
			FAAM["musicalWorks"].append(
				{
					"workName": row["\ufeffName"],
					"wikidataUrl": wikidataUrl+row["Wikidata QID"],
					"qid": row["Wikidata QID"],
					"composers": [{"agentName": row["composer"], "qid": row["composer QID"]}],
					"arrangers": [{"agentName": row["arranger"], "qid": row["arranger QID"]}],
					"annotations": [],
					"FAAM-IDs": [],
					"occurrence": 1
				}

				)
	# Generate annotations
	for row in annotations_dict["items"]:
		try:
			query = list(filter(lambda x: x[1].get('annotationName') == row["\ufeffName"], enumerate(FAAM["annotations"]) ))
			current_annotation = FAAM["annotations"][query[0][0]]
			#print(current_annotation)
			if len(query) >0:	
				# add subclass
				if any(x.get("annotationName") == row["subclass of"] for x in current_annotation["subclass_of"]):
					pass
				else:
					# append subclass
					current_annotation["subclass_of"].append(
						{
							"annotationName": row["subclass of"]				
						}

						)
				# add musical parameter
				if any(x.get("annotationName") == row["musical parameter"] for x in current_annotation["musical_parameters"]):
					pass
				else:
					# append musical parameter
					current_annotation["musical_parameters"].append(
						{
							"annotationName": row["musical parameter"]				
						}

						)
			else: # append new annotation
				FAAM["annotations"].append(
				{
					"annotationName": row["\ufeffName"],
					"wikidataUrl": wikidataUrl+row["Wikidata QID"],
					"qid": row["Wikidata QID"],
					"subclass_of": [{"annotationName": row["subclass of"]}],
					"musical_parameters": [{"annotationName": row["musical parameter"]}],
					"FAAM-IDs": [],
					"occurrence": 0
				}

				)	
		except IndexError: # first element
			FAAM["annotations"].append(
				{
					"annotationName": row["\ufeffName"],
					"wikidataUrl": wikidataUrl+row["Wikidata QID"],
					"qid": row["Wikidata QID"],
					"subclass_of": [{"annotationName": row["subclass of"]}],
					"musical_parameters": [{"annotationName": row["musical parameter"]}],
					"FAAM-IDs": [],
					"occurrence": 0
				}

				)	

	return FAAM

def faaamStatistics(FAAM): #Generates statistics for FAAM JSON
	# Unique agents, musicalWorks and annotations
	for manifestation in FAAM["manifestations"]:
		for musicalWork in manifestation["musicalWorks"]: #add manif. to musical works
			if musicalWork["workName"] == "":
				pass
			else:	
				# check if the work's Name is already present
				query = list(filter(lambda x: x[1].get('workName') == musicalWork["workName"], enumerate(FAAM["musicalWorks"])))
				if len(query) >0:
					# update occurrence
					FAAM["musicalWorks"][query[0][0]]["FAAM-IDs"].append(manifestation["FAAM-ID"])
				else:
					print("Missing musical work: \n")
					print(manifestation["FAAM-ID"])

		for agent in manifestation["agents"]: #add agent to agents list
			query = list(filter(lambda x: x.get('agentName') == agent["agentName"], FAAM["agents"]))
			if len(query)>0: # agent exists in list
				pass
			else: # create agent
				FAAM["agents"].append({
					"agentName": agent["agentName"],
					"agentRole": agent["agentRole"]
					})
		for annotation in manifestation["annotations"]: # add annotations to annotations list
			query = list(filter(lambda x: x[1].get('annotationName') == annotation["annotationName"], enumerate(FAAM["annotations"])))
			if len(query)>0:
				#print(FAAM["annotations"][query[0][0]])
				current_annotation = FAAM["annotations"][query[0][0]]
				current_annotation["FAAM-IDs"].append(manifestation["FAAM-ID"])
				current_annotation["occurrence"]+=1
			else:
				print("Missing annotation: ",annotation["annotationName"])				
	for work in FAAM["musicalWorks"]: # add qids to agents and annotations
		for composer in work["composers"]:
			query = list(filter(lambda x: x[1].get('agentName') == composer["agentName"],enumerate(FAAM["agents"])))
			if len(query)>0:
				FAAM["agents"][query[0][0]]["qid"] = composer["qid"]
		for arranger in work["arrangers"]:
			if arranger["agentName"] != "":
				query = list(filter(lambda x: x[1].get('agentName') == arranger["agentName"],enumerate(FAAM["agents"])))
				if len(query)>0:
					FAAM["agents"][query[0][0]]["qid"] = arranger["qid"]

		for faamId in work["FAAM-IDs"]:
			# append annotations
			query = list(filter(lambda x: x[1].get('FAAM-ID') == faamId, enumerate(FAAM["manifestations"])))
			for annotation in FAAM["manifestations"][query[0][0]]["annotations"]:
				query = list(filter(lambda x: x.get('annotationName') == annotation["annotationName"], work["annotations"] ))
				if len(query) > 0: # pass if already present
					pass
				else: # append new annotaion and retrieve qid
					query = list(filter(lambda x: x.get('annotationName') == annotation["annotationName"], FAAM["annotations"] ))
					if len(query)>0:
						annotation_qid = query[0]["qid"]
						work["annotations"].append({"annotationName": annotation["annotationName"], "qid": annotation_qid})
					else:
						print("Missing annotation!\n")
						print(annotation["annotationName"])





	# Base statistics
	# average arrangers / work
	sum_arrangers = 0
	sum2_arrangers = 0
	high_occurrences = []
	for work in FAAM["musicalWorks"]:
		sum_arrangers += work["occurrence"]
		sum2_arrangers += work["occurrence"]**2

	mu = float(sum_arrangers)/len(FAAM["musicalWorks"])
	mu2 = float(sum2_arrangers)/len(FAAM["musicalWorks"])
	sigma = np.sqrt(mu2-(mu)**2)
	max_occurrence = mu + sigma
	for work in FAAM["musicalWorks"]:
		if work["occurrence"] >= max_occurrence:
			high_occurrences.append({"workName": work["workName"], "occurrence": work["occurrence"]})

	FAAM["statistics"] = {
	"averageArrangersPerWork": mu,
	"standardDeviationArrangersPerWork": sigma,
	"highOccurrenceWorks": high_occurrences
	}	

				
	return FAAM



# CODE
#print("Insert the input CSV filename (with extension): \n")
#input_csv_filename = input()
#TEST
date = "20250131"

input_manifestations_csv_filename = "FAAM-scarlatti_export_"+date+".csv"
input_works_csv_filename = "FAAM-scarlatti_works_export_"+date+".csv"
input_annotations_csv_filename = "../FAAM_annotations/FAAM-annotations_export-"+date+".csv"
output_json_filename = input_manifestations_csv_filename[:-4]+".json"
network_json_filename = "FAAM-network_"+date+".json"
network_visualisation_filename = "FAAM-network_"+date+".html"

print("Loading CSVs into Python dictionary...")
manifestations_dict = csv2dict(input_manifestations_csv_filename)
works_dict = csv2dict(input_works_csv_filename)
annotations_dict = csv2dict(input_annotations_csv_filename)

print("Clean-up and export to JSON...")
FAAM = inputCsv2faamJson(manifestations_dict,works_dict,annotations_dict)
FAAM = faaamStatistics(FAAM)
dict2json(FAAM,output_json_filename)

print("Generating Graph network...")
net = generate_network(FAAM)
network_dict = nx.node_link_data(net)
network_file = open(network_json_filename,'w')
json.dump(network_dict,network_file,indent=2)
pyvis_visualization(net,network_visualisation_filename)

print("Generating charts for statistics...")
# create input list
x_list = []
y_list = []
sortedHighOccurrenceWorks = sorted(FAAM["statistics"]["highOccurrenceWorks"], key=lambda x:x['occurrence'])
x_list = list(map(lambda x: x.get('occurrence'),sortedHighOccurrenceWorks))
y_list = list(map(lambda x: x.get('workName'),sortedHighOccurrenceWorks))
# filter the first 10 works
xy_horizontalhistogram(x_list[-12:],y_list[-12:],"Occurence","Works with high occurrence")
