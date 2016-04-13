from queue import Queue
from graph_builder import graph_build
from graph import WeightedGraph

class graph_info:
    '''
    Create class that holds all the map information:
        g: original graph
        route_graph: current order of source and destination routes
        coord: coordinate list
        path_dict: current order of waypoints to be visited
    '''
    def __init__ (self):
        self.g, self.coord = graph_build()
        self.route_graph = WeightedGraph()
        self.s_name_text = ""
        self.d_name_text = ""

        self.new_path = False
        self.address_q = Queue()
        self.waypoints = []
        self.sd_dict = dict()
        self.path_dict = dict()
        self.name_vert_dict = dict()

        self.sd_list = set()
        self.ordered_list = []
        self.master_path = []
        
        
        