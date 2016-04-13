from route_builder import route_builder
from wp2pixels import wayp2draw, destinations
import threading
import time
from graph import WeightedGraph
from graph_builder import *
import copy

class route_thread(threading.Thread):
    '''
    route thread is the multi-threading class that defines which
    processes are run when the route thread is initialized
    Process:
        route_thread calls the route builder to find the least cost
        path between all source/destinations and ultimately the 
        best path to pick up and deliver items through a restricted
        travelling salesman algorithm.
    '''
    def __init__(self, args):
        '''
        Initialize thread, and assign proper arguments
        '''
        threading.Thread.__init__(self)
        self.route_info = args
    def run(self):
        '''
        Allow for more source destinations to be added
        while calculating the least cost paths before
        calculating the next tsp by using a stop
        '''
        self._stop = threading.Event()
        route_builder(self.route_info,self._stop)
        return


class draw_thread(threading.Thread):
    '''
    draw_thread is the multi-threading class that manipulates
    the path on the canvas and the waypoints on the waypoint
    list
    '''
    def __init__(self, args):
        '''
        Initialize thread, and assign proper arguments
        '''
        threading.Thread.__init__(self)
        self.route_info = args[0]
        self.canvas = args[1]
        self.wayp_list_display = args[2]
    def run(self):
        '''
        -Draw the initial path
        -Manipulate a prior path
        -Simulate a car driving on the path
        -Finish path and prepare variables for next call
        '''
        initiated = False                                                                                                       # initialize the path, before travelling along the path
        while True:                                                                                                             # continuous path drawer
            if self.route_info.waypoints and self.route_info.new_path:                                                          # if there are waypoints and there is a new path to draw
                try:                                                                                                            # try to delete any old paths that may be currently on the canvas
                    self.canvas.delete("route")
                except:
                    print("No Prior Route To Delete") 
                self.canvas.create_line(wayp2draw(self.route_info.coord, self.route_info.waypoints), tag="route")               # draw path
                
                temp = copy.deepcopy(self.route_info.ordered_list)
                for sd in temp:
                    self.canvas.create_oval(destinations(self.route_info.coord, sd), tag="dest")
                
                self.route_info.new_path = False                                                                                # set new path back to no new path to draw (False)
                if self.wayp_list_display.size() != len(self.route_info.ordered_list):                                          # Now the path has been initialized
                    self.wayp_list_display.delete(0,"end")
                    for counter,sd in enumerate(self.route_info.ordered_list):
                        try:
                            temp_string = str(self.route_info.name_vert_dict[sd])
                            self.wayp_list_display.insert(counter, temp_string)                                                 # Insert name into list
                        except:
                            print("No Name Linked to Vertice")                                                                  
                initiated = True                                                                                                
                i,j = 0,1                                                                                                       # travelling starting variables
                curr_dist = 0
                wayp_dist = deg2km(cost_distance(self.route_info.coord, 
                                                 self.route_info.waypoints[i], self.route_info.waypoints[j]))                   # find the initial waypoint distance between waypoint[0] and waypoint[1]
                t_diff = time.clock()                                                                                           # start driving, initialize the clock
                
                
            if self.route_info.waypoints and initiated:                                                                         # function must have waypoints and be initialized to start driving
                t_dist = time.clock() - t_diff                                                                                  # find time travelled
                t_diff = time.clock()                                                                                           # travelling at 800 km/h, therefore d = vt
                curr_dist += t_dist*float(150/3600)
                if curr_dist >= wayp_dist:                                                                                      # if the curr_dist is greater than the waypoint distance go to next subsegment
                    i += 1  
                    j += 1
                    if j < len(self.route_info.waypoints):                                                                      # if no waypoints left to iterate go to end path
                        curr_dist -= wayp_dist                                                                                  # minus subsegment distance from current distance
                        wayp_dist = deg2km(cost_distance(self.route_info.coord, 
                                                         self.route_info.waypoints[i], self.route_info.waypoints[j]))           # find next waypoint distance
                        if self.route_info.waypoints[0] in self.route_info.ordered_list:                                        # if the most recent waypoint is a source or destination
                            self.route_info.master_path = self.route_info.waypoints[0:self.route_info.waypoints.index(self.route_info.ordered_list[1])]
                            temp_waypoint = self.route_info.waypoints[0]                                                        # save waypoint to be deleted from all data points 
                            self.route_info.ordered_list.remove(temp_waypoint)                                                  # remove from ordered list
                            self.wayp_list_display.delete(0, "end")                                                             # delete all names in list
                            for counter,sd in enumerate(self.route_info.ordered_list):                                          # print new list
                                try:
                                    temp_string = str(self.route_info.name_vert_dict[sd])
                                    self.wayp_list_display.insert(counter, temp_string)
                                except:
                                    print("No Name Linked to Vertice")
                            try:
                                if temp_waypoint not in self.route_info.ordered_list:                                           # only if the waypoint no longer appears in the list then delete
                                    self.route_info.sd_list.remove(self.route_info.waypoints[0])           
                            except:
                                print("Initial Node was removed prior ***")
                            self.canvas.delete("dest")                                                                          # delete destination labels
                            for sd in self.route_info.ordered_list:                                                             # store remaining destinations
                                self.canvas.create_oval(destinations(self.route_info.coord, sd), tag="dest")
                        self.route_info.waypoints.remove(self.route_info.waypoints[0])                                          # remove the waypoint past
                    else:
                        try:
                            self.canvas.delete("route")                                                                         # delete what's left of the route
                            self.canvas.delete("dest")                                                                          # delete the remaining destination
                            self.wayp_list_display.delete(0, "end")                                                             # delete all elements in the list
                        except:
                            print("All artifacts already gone.")                                                                
                        self.route_info.waypoints = []                                                                          # reset variables
                        self.route_info.master_path = []
                        self.route_info.sd_list = set()
                        self.route_info.ordered_list = [self.route_info.ordered_list[-1]]                                       # store the last possible location for the new current location
                        i,j = 0, 1
                        initiated = False                                                                                       # no path is now initialized on the canvas
                    self.route_info.new_path = True                                                                             # draw the empty path to make sure
