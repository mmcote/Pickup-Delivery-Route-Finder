import tkinter as tk
from tkinter import ttk
from tkinter import font
from graph_builder import mult_coords

from graph_information import graph_info
import threading
from queue import Queue
import threads

class food_delivery_app(tk.Tk):
    '''
    Core module of the delivery app bringing together both
    front end and back end modules.
    '''
    def __init__(self, *args, **kwargs):
        # initialize tkinter too
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Food Delivery Route Finder")         # title to be shown on window bar
        tk.Tk.wm_geometry(self, newGeometry = "1216x656+30+30")    # sets size of window
        tk.Tk.wm_resizable(self, width = False, height = False)
        
        # initialize main frame for window
        container = tk.Frame(self)    
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        # initialize the main_page frame
        frame = main_page(container, self)     
        self.frames[main_page] = frame
        frame.grid(row = 0, column = 0, sticky = "nsew")

        # bring frame requested to view
        self.front_frame(main_page)

    def front_frame(self, page):
        # allow for multiple pages
        frame = self.frames[page]
        frame.tkraise()

class main_page(tk.Frame):
    '''
    Initial page showing the map, path, and inputs for new
    source and destinations
    '''
    
    def __init__(self, parent_class, controller):
        '''
        Initializes frame for main page
        '''
        tk.Frame.__init__(self, parent_class)
        self.route_info = graph_info()     # route_info is a graph_info class; it contains information to be passed between files and threads
        self.map_widget()                  # calls to map_widget() function to display widgets on window

    def map_widget(self):
        '''
        Initializes the widgets used for the GUI. 
        '''
        # must be a global variable or else image will be collected as "garbage"
        global map_image
        global s_text_entry
        global d_text_entry
        global s_name_text_entry
        global d_name_text_entry
        
        map_image = tk.PhotoImage(file = "edmonton_map.png")    # assign photo to be used as image for map to be displayed
        
        # initialize frame for the map image
        self.map_frame = tk.Frame(self, height = 600, width = 600)
        self.map_frame.place(x = 580, y = 20)    # place frame on window
        
        # initialize canvas to display map image (allows drawing on the map to display 'driving')
        self.canvas = tk.Canvas(self.map_frame, height = 600, width = 600)
        self.canvas.create_image(0, 0, image = map_image, anchor="nw")    # puts map image on canvas
        
        # intialize scrollbars for the map (allows user to scroll around the map)
        self.xsb = tk.Scrollbar(self.map_frame, orient = "horizontal", command = self.canvas.xview)
        self.ysb = tk.Scrollbar(self.map_frame, orient = "vertical", command = self.canvas.yview)
        
        self.canvas.configure(yscrollcommand = self.ysb.set, xscrollcommand = self.xsb.set)    # gives funcionality to the scrollbars
        self.canvas.configure(scrollregion = (0,0,1320,1212))    # makes the whole canvas scrollable

        self.xsb.pack(side = "bottom", fill = "x")    # place horizontal scrollbar at bottom
        self.ysb.pack(side = "right", fill = "y")     # place vertical scrollbar at the right side
        self.canvas.pack()    # pack the canvas onto the window so that it displays
                
        # frame for the UI (where the user inputs source and destination addresses and names)
        self.ui_frame = tk.Frame(self, height = 200, width = 550)
        self.ui_frame.place(x = 15, y = 450)
        self.helv16 = font.Font(family = "helvetica", size = 16, weight = "bold")    # initializes font to be used when displaying text
        
        # frame for the waypoints list (displays all the places visited by driver)
        self.wayp_window = tk.Frame(self, height = 450, width = 600)
        self.wayp_window.place(x = 15, y = 20)
        self.wayp_list_display = tk.Listbox(self.wayp_window, font = self.helv16, height = 15, width = 45)    # initialize listbox to display text
        
        # initialize scrollbar for the Listbox (allow user to scroll once amount of waypoints to be displayed fills up box)
        self.y_scroll = tk.Scrollbar(self.wayp_window, orient = "vertical", command = self.wayp_list_display.yview)
        self.wayp_list_display.configure(yscrollcommand = self.y_scroll.set)
        self.y_scroll.pack(side = "right", fill = "y")    # place the scrollbar to the right of the listbox
        
        self.wayp_list_display.pack()    # pack listbox so that it displays on window
        
        # StringVar instance gets the user input from the Entry widgets
        s_text_entry = tk.StringVar()         # gets input for source addresses
        d_text_entry = tk.StringVar()         # gets input for destination addresses
        s_name_text_entry = tk.StringVar()    # gets input for the name of the source location
        d_name_text_entry = tk.StringVar()    # gets input for the name of the destination location
        
        # thread for drawing is initialized it is passed the route_info, canvas, and wayp_list and will run (make window and widgets functional)
        #  while the routes are being calculated/built
        drawing = threads.draw_thread(args = (self.route_info, self.canvas, self.wayp_list_display))
        drawing.start()    # starts the thread
        
        # displays text on the window prompting user to enter source and destination locations
        self.source_prompt = tk.Label(self.ui_frame, text = "Source: ", font = self.helv16).place(x = 42, y = 25)
        self.destination_prompt = tk.Label(self.ui_frame, text = "Destination: ", font = self.helv16).place(x = 0, y = 80)
        
        # uses Entry widget that allows user to input entries to a text box and displays them beside respective source location and name prompts
        self.source_name_entry = tk.Entry(self.ui_frame, textvariable = s_name_text_entry, font = self.helv16).place(x = 135, y = 25)
        self.source_entry = tk.Entry(self.ui_frame, textvariable = s_text_entry, font = self.helv16).place(x = 135, y = 50)
        
        # uses Entry widget that allows user to input entries to a text box and displays them beside respective destination location and name prompts
        self.destination_name_entry = tk.Entry(self.ui_frame, textvariable = d_name_text_entry, font = self.helv16).place(x = 135, y = 85)
        self.destination_entry = tk.Entry(self.ui_frame, textvariable = d_text_entry, font = self.helv16).place(x = 135, y = 110)
        
        # uses Button widget that allows user to press a button to confirm entries
        # calls to sd_input upon button pressed
        self.enter_button = tk.Button(self.ui_frame, text = "Enter", font = self.helv16, command = self.sd_input, fg = "white", bg = "red")
        self.enter_button.place(x = 395, y = 20)
        self.enter_button.configure(height = 2, width = 8)

    
    def sd_input(self):
        '''
        Upon pressing the button from the map_widget, this function will be called.
        It will pass the necessary information needed to route_info that need to be used when building routes.
        The route_thread will also be started for calculating the routes
        '''
        # contains the user input for source and destination respectively
        self.route_info.s_name_text = s_name_text_entry.get()
        self.route_info.address_q.put(s_text_entry.get())    # pushes to queue address of source
        self.route_info.d_name_text = d_name_text_entry.get()
        self.route_info.address_q.put(d_text_entry.get())    # pushes to queue address of destination
        
        # will look if there is already a thread; if so, it will keep the current thread as the running one;
        # otherwise, a new one will be created and ran
        curr_thread = threading.enumerate()
        curr_thread = [x for x in threading.enumerate() if isinstance(x, threads.route_thread)]
        
        if len(curr_thread) > 0:
            curr_thread[0].Event.set()
        else:
            route = threads.route_thread(args=(self.route_info))
            route.start()   

if __name__ == "__main__":
    # runs window
    app = food_delivery_app()
    app.mainloop()
