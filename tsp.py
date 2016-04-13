from graph import WeightedGraph
import copy
import math

def tsp_dp(func, memo = None):
    '''
    tsp decorator to memoize the tsp algorithm by remembering the 
    inputs and calling on the memo is similar arguments are 
    called again
    '''
    if memo == None:
        memo = dict()
    def memo_wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)                # find tsp if the arguments are not in memo, and store
        return copy.deepcopy(memo[args])
    return memo_wrapper                            

@tsp_dp    
def tsp(start, subset, route_info):
    subset = set(subset)
    '''
    Get the path of minimum length that starts at city 0, passes
    through the set of cities 1 to n in any order and ends at
    city 0.
    '''
    if len(subset) == 1:
        end = subset.pop()                          # base case where if there is only two elements get the weight
        return [(start, end)], route_info.route_graph.get_weight(start,end)
    else:
        path = None                                 # start as an empty path
        for vert in subset:
            temp_subset = copy.deepcopy(subset)
            temp_subset.remove(vert)
            temp_subset = frozenset(temp_subset)    # needs to be hashable
            connection, dist = tsp(vert, temp_subset, route_info)                           # call function over again with smaller subset
            total_dist = dist + route_info.route_graph.get_weight(start,vert)               # add up total distance
            if start in route_info.sd_dict:                                                 # check if source is alread in path
                if path:
                    dest_contained = [item for item in path[0] if item[0] == route_info.sd_dict[start]]
                    if dest_contained:                                                      
                        total_dist = float("inf")                                            # set to infinity as there will be a better path
                else:
                    total_dist = float("inf")
            connection.append((start,vert))                                                  # append the new vertice for the hypothetical path thus far
            if not path or total_dist < path[1]:                                             # append if the new route is cheaper than the prior
                path = (connection, total_dist)                                              # set to current path in this level of recursion
        return path 
