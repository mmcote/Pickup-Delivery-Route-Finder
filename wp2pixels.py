from route_builder import mult_coords
import math

def deg2pixel(coordinates):
    '''
    Converts the coordinate degrees to pixels for drawing on the map.
    '''
    lat, lon = (coord for coord in coordinates)
    
    # equations for converting from degrees to pixels
    lat = mult_coords(53.670224) - lat    
    lon = lon - mult_coords(-113.695070)
    lon_pix = lon*0.02910
    lat_pix = lat*0.04915
    
    return lon_pix, lat_pix

def wayp2draw(coord_dict, wayp_list):
    pixel_route = []
    prior = wayp_list[0]
    pri_lat, pri_lon = coord_dict[prior]
    for i in wayp_list:
        if i == prior:
            continue
        else:
            temp_lat, temp_lon = deg2pixel((pri_lat,pri_lon))
            pixel_route.append(temp_lat)
            pixel_route.append(temp_lon)
            curr_lat, curr_lon = coord_dict[i]
            temp_lat, temp_lon = deg2pixel((curr_lat,curr_lon))
            pixel_route.append(temp_lat)
            pixel_route.append(temp_lon)            
            if i != wayp_list[-1]:
                pri_lat = curr_lat
                pri_lon = curr_lon
            else:
                break

    return tuple(pixel_route)

def destinations(coord_dict, sd):
    pixel_route = []
    temp_lat, temp_lon = deg2pixel(coord_dict[sd])
    pixel_route.append(temp_lat + 5)
    pixel_route.append(temp_lon - 5)
    pixel_route.append(temp_lat - 5)
    pixel_route.append(temp_lon + 5)  
    return tuple(pixel_route)

