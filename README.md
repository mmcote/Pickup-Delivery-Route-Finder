# Pickup-Delivery-Route-Finder-
CMPUT 275 Final Project: Find an the most efficient order and route to pickup and deliver multiple orders, a variation of the travelling salesman problem. The interface is made with tkinter, and the ease of use can be attributed to simple multithreading with the build in multithreading module.

The purpose of this project is to find the shortest route to deliver multiple food orders around the city of Edmonton. A modified version of the Travelling Salesman Problem will be the basis of this project. Several elements from Assignment #1 will also be used (the Graph class, leastcostpath (Dijkstra's algorithm), etc.). A GUI will also be implemented to display a drawing of the driver's route and a simulation of the driver along the route picking up and delivering the items.

To Run:
    Install pip for python3:
        - Download the get-pip.py file to your virtual machine. This can be downloaded from:
        https://pip.pypa.io/en/stable/installing/
        - Then enter the command:
            sudo python3 get-pip.py
            - This will install pip as pip3.4
    Install geopy:    
        - Enter the command: 
            sudo pip3.4 install geopy
            - This will install the latest version of geopy, version 1.11.0.
    
    RUN THE PROGRAM:
        - Go to the directory of the main.py
        - Enter the command python3 main.py
        
To Use:
    - There are 4 input boxes:
        -The first two belong to the source.
            -The first of two boxes are for the nickname of the source location, eg. KFC.
            -The secnod of two boxes are for the address of the source location, eg. 9473 19 Ave NW, Edmonton, AB.
        -The last two belong to the destination.
            -The first of two boxes are for the nickname of the destination location, eg. Mike's House.
            -The second of two boxes are for the address of the destination location, eg. 8882 170 St NW, Edmonton, AB.
    - The accessory geocoder used by the application provided by geopy takes in addresses only in a specific format.
    - For example:
        If by street number:
            eg. 9473 19 Ave NW, Edmonton, AB
        Or by avenue number:
            eg. 8882 170 St NW, Edmonton, AB
    - The geocoder does not take in zip codes or nicknames for streets such as Jasper Avenue
    - Only after the source and destination have been entered should you hit the enter button.
    - While the route is being calculated you can feel free to browse the prior routes or the map as the program is multithreaded and allows for the dual-processes. 
    - Once the route is done being calculated the route will appear on the map, as can be seen the route will slowly dissapear. This is to simulate a car driving the route. Source and destinations are marked by small 4 pixel circles. The car is set to be driving at 150 km/h. As can be seen when the route is done being calculated, the source and destinations will appear in the table in the top left. They are in order of places to visit, as you can see sources will always be before destinations as the food needs to be picked up.
