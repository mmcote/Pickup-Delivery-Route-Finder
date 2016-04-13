'''https://github.com/geopy/geopy'''
from geopy.geocoders import Nominatim
from graph_builder import *
from graph import WeightedGraph
from tsp import tsp
import copy
import threading

def route_builder(route_info, stop):
    def append_graph(route_info, stop):
        # initiate geocoder wrapper
        geolocator = Nominatim()
        # get the geocode object from the geopy to convert these string addresses to there respective lat/lon coordinates
        source = geolocator.geocode(route_info.address_q.get())
        destination = geolocator.geocode(route_info.address_q.get())

        # both source and destination cannot be none as if they are none, this means that the addresses inputted were in the wrong format
        # and no geocode could be found for the addresses
        if source and destination:
            print("Valid Source and Destination")
            if route_info.ordered_list:
                current_location = route_info.ordered_list[0]
            else:
                # default location to start the program, approximately in the middle of the city
                current_location = geolocator.geocode("10127 121 St NW, Edmonton, AB")
                current_location = find_vertex(route_info.coord, mult_coords(current_location.latitude),mult_coords(current_location.longitude)) 
                route_info.name_vert_dict[current_location] = "10127 121 St NW, Edmonton, AB"
            route_info.sd_list.add(current_location)

            # find the closest vertices in the graph for the source and destination, thereafter find the least cost path through dijkstra's algorithm
            source = find_vertex(route_info.coord, mult_coords(source.latitude),mult_coords(source.longitude))
            destination = find_vertex(route_info.coord, mult_coords(destination.latitude), mult_coords(destination.longitude))
            
            # store the name of the location corresponding to the vertice
            route_info.name_vert_dict[source] = route_info.s_name_text
            route_info.name_vert_dict[destination] = route_info.d_name_text

            min_path, path_dist = least_cost_path(route_info.g, route_info.coord, source, destination, cost_distance)
            temp_list = copy.deepcopy(set(route_info.sd_list))
            # create an edge with the least cost path between all prior source and destinations using dijkstra's algorithm
            for vert in temp_list:
                # source to vert
                temp_min_path, temp_path_dist = least_cost_path(route_info.g, route_info.coord, min_path[0], vert, cost_distance)
                route_info.route_graph.add_edge(min_path[0], vert, temp_path_dist[1])
                route_info.path_dict[(min_path[0], vert)] = temp_min_path
                # vert to start
                temp_min_path, temp_path_dist = least_cost_path(route_info.g, route_info.coord, vert, min_path[0], cost_distance)
                route_info.route_graph.add_edge(vert, min_path[0], temp_path_dist[1])
                route_info.path_dict[(vert, min_path[0])] = temp_min_path
                # destination to vert
                temp_min_path, temp_path_dist = least_cost_path(route_info.g, route_info.coord, min_path[-1], vert, cost_distance)
                route_info.route_graph.add_edge(min_path[-1], vert, temp_path_dist[1])
                route_info.path_dict[(min_path[-1], vert)] = temp_min_path
                # vert to destination
                temp_min_path, temp_path_dist = least_cost_path(route_info.g, route_info.coord, vert, min_path[-1], cost_distance)
                route_info.route_graph.add_edge(vert, min_path[-1], temp_path_dist[1])
                route_info.path_dict[(vert, min_path[-1])] = temp_min_path
            
            # create final edge from source to destination
            route_info.route_graph.add_edge(min_path[0],min_path[-1],path_dist[1])
            # add to destination dictionary, destination is key and source is value to ensure that source always comes before destination in tsp
            route_info.sd_dict[min_path[-1]] = min_path[0]
            # save the associated least cost path waypoints to the path dictionary
            route_info.path_dict[(min_path[0], min_path[-1])] = min_path
            # add the source vertex to the source destination list
            route_info.sd_list.add(source)
            # add the destination vertex to the source destination list
            route_info.sd_list.add(destination)
            # return the value used for the current location during calculation
            return current_location
    # call the append new source and destination function
    current_location = append_graph(route_info, stop)
    # if while calculating the last append graph, another request was made add the new source, destination before calculating the tsp
    while stop.isSet():
        current_location = append_graph(route_info, stop)
        stop = threading.Event()
    # list of vertices to find tsp between, with the starting location as the current location
    temp_set = route_info.sd_list
    try:
        temp_set.remove(current_location)
    except:
        print("Past the next waypoint")
    # find the tsp from starting from the current location
    final_path, final_dist = tsp(current_location, frozenset(temp_set), route_info)
    final_path.reverse()
    # depending on the location of the car will the next starting path from the where the car currently is will be decided
    if current_location in route_info.waypoints:
        prior_waypoints = route_info.waypoints[0:route_info.waypoints.index(current_location)]
    elif route_info.waypoints:
        # if the car passes the next waypoint intended for by the time the route is calculated return to waypoint then go on ts path
        # this is assuming that the car will not exceed the point by much, a simplification on drawing
        route_info.master_path.reverse()
        prior_waypoints = route_info.master_path[route_info.master_path.index(route_info.waypoints[0]):]
    else:
        prior_waypoints = []
    
    temp = final_path[0]
    # make final waypoint path for driving
    route_info.waypoints = prior_waypoints + route_info.path_dict[temp][0:]
    route_info.ordered_list = []
    route_info.ordered_list.append(temp[0])
    final_path.remove(temp)
    # create ordered list of source and destinations to check off
    for x in final_path:
        route_info.ordered_list.append(x[0])
        route_info.waypoints = route_info.waypoints + route_info.path_dict[x][1:]

    route_info.ordered_list.append(final_path[-1][1])
    # ready to draw and drive the new path
    route_info.new_path = True
    return