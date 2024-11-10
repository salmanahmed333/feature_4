# Import necessary libraries
import streamlit as streamlit_app

# SignalClass for managing details of signals at traffic junctions
class SignalClass:
    def __init__(self, pos, coords):
        self.pos = pos
        self.coords = coords
        self.is_active = False  # False represents Red, True represents Green
        self.signal_status = False  # Red by default
    
    def flip_status(self):
        if self.signal_status:
            self.signal_status = False
        else:
            self.signal_status = True
    
    def display_info(self):
        info = {
            "Position": self.pos,
            "Latitude": self.coords[0],
            "Longitude": self.coords[1],
            "Status": "Green" if self.signal_status else "Red"
        }
        return info

# StreetClass to manage information about streets and signals on those streets
class StreetClass:
    def __init__(self, road_name, road_direction, coord_start, coord_end, road_length):
        self.road_name = road_name
        self.road_direction = road_direction
        self.coord_start = coord_start
        self.coord_end = coord_end
        self.road_length = road_length
        self.traffic_signal = None
        self.signal_object = None
    
    def attach_traffic_signal(self):
        self.traffic_signal = SignalClass(self.road_direction, self.coord_end)
    
    def display_road_info(self):
        road_info = {
            "Street Name": self.road_name,
            "Direction": self.road_direction,
            "Start Coordinate": self.coord_start,
            "End Coordinate": self.coord_end,
            "Length of Street": self.road_length
        }
        if self.traffic_signal:
            road_info["Signal Info"] = self.traffic_signal.display_info()
        return road_info

# Intersection class that uses streets in a more complex structure
class Intersection:
    def __init__(self, identifier, street_collection):
        self.identifier = identifier
        self.street_collection = street_collection
    
    def get_info_of_intersection(self):
        intersection_info = {"Intersection ID": self.identifier, "Street Details": []}
        for strt in self.street_collection:
            intersection_info["Street Details"].append(strt.display_road_info())
        return intersection_info

# Function for Streamlit to display signal information
def show_signal_information(signal_instance):
    info = signal_instance.display_info()
    streamlit_app.write("Signal Position:", info["Position"])
    streamlit_app.write("Latitude:", info["Latitude"])
    streamlit_app.write("Longitude:", info["Longitude"])
    streamlit_app.write("Current Status:", info["Status"])

# Streamlit application layout to showcase street, signal, and intersection info
def run_application():
    streamlit_app.title("Traffic Signal Management System")

    # Create example streets and intersections
    street_one = StreetClass("Cicero Ave", "Southbound", (41.8797, -87.8045), (41.8942, -87.8051), 1.01)
    street_two = StreetClass("Main St", "Northbound", (41.8790, -87.8030), (41.8935, -87.8065), 1.20)
    intersection_one = Intersection("Intersection 1", [street_one, street_two])
    
    # Add traffic signal to the street and showcase details
    street_one.attach_traffic_signal()
    streamlit_app.subheader("Street Information Section")
    streamlit_app.json(street_one.display_road_info())

    # Allow toggling signal status and display updated signal status
    if street_one.traffic_signal:
        if streamlit_app.button("Change Signal Status for Cicero Ave"):
            street_one.traffic_signal.flip_status()
        show_signal_information(street_one.traffic_signal)

    # Display intersection details
    streamlit_app.subheader("Intersection Details Section")
    streamlit_app.json(intersection_one.get_info_of_intersection())

if __name__ == "__main__":
    run_application()
