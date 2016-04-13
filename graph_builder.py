from graph import Graph
from minheap import MinHeap
from math import pow
from math import sqrt

def mult_coords(latORlon):
    return int(float(latORlon)*100000)

def deg2km(deg):
    return float(deg/100000)*110

def graph_build():
	'''Builds a directed graph from edmonton-roads-2.0.1.txt file, a CSV file.
	It reads and stores the file values appropriately for use in the program.
	'''
	g = Graph()
	coord = dict()	# coord must be a dictionary with keys as the vert ID's

	with open('edmonton-roads-2.0.1.txt') as file:			# access the text file
		waypoints = [line.strip().split(',') for line in file]	# split by comma and remove the ending new line character
		for line in waypoints:					# faster to read and store the file values than take in each and operate on each
			ve,v1,v2ORlat,lon = line
			if ve == 'V':					# vertex
				g.add_vertex(v1)
				coord[v1] = (int(float(v2ORlat)*100000),int(float(lon)*100000))
			elif ve == 'E':					# edge
				g.add_edge(v1, v2ORlat)
				
	return g, coord							# no need to return anything


def find_vertex(coordList, lat, lon):
	'''Finds closest vertex to given coordinate inputs.
	It takes in the list of coordinates stored and the latitude
	and longitude from stdin. It returns the vertex ID of the closest
	point.
	'''
	# assigns minimum vertex ID and coordinates for point from list of stored coordinates
	min_vert = list(coordList.keys())[0]		# puts stored vertices into list
	min_coord = coordList.get(min_vert)		# obtains values of given vertice in coordList dictionary (lat, lon)
	min_lat, min_lon = min_coord			# stores respective lat/lon
	
	min_dist = sqrt(pow((lat - min_lat),2) + pow((lon - min_lon),2))	# initialize minimum distance
	# finds vertex based on calculated minimum distance above from user.
	for vert_id, ind_coord in coordList.items():				
		ind_lat, ind_lon = ind_coord		# takes lat/lon from coordList dictionary
		distance = sqrt(pow((lat - ind_lat),2) + pow((lon - ind_lon),2))	# calculates distance
		# compares minimum distance to calculated distance
		if distance <= min_dist:			# calculated distance has to be less than/equal to min distance
			min_dist = distance			# if condition met, minimum distance becomes the calc distance
			min_vert = vert_id			# minimum vertice is now the vert ID
	vertex = min_vert					# closest vertex has been found
	
	return vertex


def cost_distance (coord, u, v):
	'''The output was assumed to be in iteger format of 100000th of a degree.
	This function uses two functions in the standard python math library pow and abs, representative
	of the power and absolute value function.
	'''
	u = str(u)			# The ID's are in the format of strings
	v = str(v)
	
	lat1, lon1 = coord[u]
	lat2, lon2 = coord[v]
	eucl = int(sqrt( pow((lat2 - lat1), 2) + pow((lon2 - lon1), 2) ))
	
	return eucl			# return euclidean distance


def least_cost_path (graph, coord, start, dest, cost):
	'''This function takes in any graph supplied by the user, by default the only graph built by the 
	script is the edmonton roads graph. This function can also take in any cost function of two 
	variables, start and destination. 
	'''
	heap = MinHeap()				# create a min heap
	heap.add(0, (start, start)) 			# dist, (vertice, prior vertice)
	reached = {}					# dictionary of vertices reached with their shortest cost and prior vertice
	while not heap.isempty():			# run the program until the heap is empty
		curr_dist, (curr_vert, pri_vert) = heap.pop_min()	# pop the min cost vertice and explore it, aka extract minimum distance runner
		for v in graph.neighbours(curr_vert):
			temp_dist = curr_dist + cost(coord, curr_vert, v) 					# Find new distance            
			if (v in reached and temp_dist < reached[v][1]) or v not in reached:		# Check if the key has been used already
				reached[v] = (curr_vert, temp_dist)	# Previous Vertice, distance
				if v != dest:
					heap.add(temp_dist, (v, curr_vert))	
	
	min_path = []				# Trace back the shortest path
	
	if dest in reached:			# First check if there is even a path
		min_path.insert(0,dest)		
		curr_id = reached[dest][0]
		prior_id = dest
		while prior_id != start:		# trace back until we reach the start from dest
			min_path.insert(0,curr_id)	# keep adding prior vert to front of list
			prior_id = curr_id
			if prior_id not in reached:	
				return min_path
			curr_id = reached[prior_id][0]
			
	return min_path, reached[dest]
